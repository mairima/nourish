import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    confirmation_sent = models.BooleanField(default=False)

    # Link orders to profiles (so profile.orders.all() works)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    class Meta:
        ordering = ["-date"]  # convenient for history lists

    def _generate_order_number(self):
        """Generate a random, unique order number using UUID."""
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = (
            self.lineitems.aggregate(Sum("lineitem_total"))["lineitem_total__sum"] or 0
        )
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = (
                self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            )
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save(update_fields=["order_total", "delivery_cost", "grand_total"])

    def save(self, *args, **kwargs):
        """
        Override save to ensure:
        - order_number is set
        - user_profile is auto-attached by matching the order email to a User's email
          (only if user_profile is empty). This makes profile.orders appear even
          for guest checkouts once a profile with the same email exists.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()

        # Auto-link to profile by email if not already linked
        if self.user_profile_id is None and self.email:
            # Avoid circular imports & be lenient on case
            try:
                matching_profile = UserProfile.objects.select_related("user").filter(
                    user__email__iexact=self.email.strip()
                ).first()
                if matching_profile:
                    self.user_profile = matching_profile
            except Exception:
                # don't block order saving if anything goes wrong
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE, related_name="lineitems"
    )
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    # Example sizes: XS, S, M, L, XL
    product_size = models.CharField(max_length=2, null=True, blank=True)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False
    )

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)
        # ensure order totals reflect this line item
        self.order.update_total()

    def __str__(self):
        """
        Don’t assume Product has `sku`. Use name when available, else the product id.
        """
        label = getattr(self.product, "name", None) or f"ID {self.product_id}"
        size = f" (size {self.product_size})" if self.product_size else ""
        return f"{label}{size} × {self.quantity} on order {self.order.order_number}"
