from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    # ---------- Utility helpers ----------

    def _order_exists_query(self, shipping_details, billing_details, grand_total, bag, pid):
        """
        Build a filter dict to check if an order already exists.
        If the Order model has original_bag / stripe_pid, include them; otherwise omit.
        """
        base = {
            "full_name__iexact": shipping_details.name,
            "email__iexact": billing_details.email,
            "phone_number__iexact": shipping_details.phone,
            "country__iexact": shipping_details.address.country,
            "postcode__iexact": shipping_details.address.postal_code,
            "town_or_city__iexact": shipping_details.address.city,
            "street_address1__iexact": shipping_details.address.line1,
            "street_address2__iexact": shipping_details.address.line2,
            "county__iexact": shipping_details.address.state,
            "grand_total": grand_total,
        }
        # include optional fields if present on the model
        if hasattr(Order, "original_bag"):
            base["original_bag"] = bag
        if hasattr(Order, "stripe_pid"):
            base["stripe_pid"] = pid
        return base

    def _order_create_kwargs(self, shipping_details, billing_details, grand_total, bag, pid, profile):
        """
        Build kwargs for creating a new Order instance.
        Only include optional fields if the model actually has them.
        """
        data = {
            "full_name": shipping_details.name,
            "user_profile": profile,
            "email": billing_details.email,
            "phone_number": shipping_details.phone,
            "country": shipping_details.address.country,
            "postcode": shipping_details.address.postal_code,
            "town_or_city": shipping_details.address.city,
            "street_address1": shipping_details.address.line1,
            "street_address2": shipping_details.address.line2,
            "county": shipping_details.address.state,
            "grand_total": grand_total,
        }
        if hasattr(Order, "original_bag"):
            data["original_bag"] = bag
        if hasattr(Order, "stripe_pid"):
            data["stripe_pid"] = pid
        return data

    # ---------- Handlers ----------

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event."""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe."""
        intent = event.data.object
        pid = intent.id
        bag = getattr(intent.metadata, "bag", "{}")
        save_info = getattr(intent.metadata, "save_info", "")

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # Clean shipping address: convert empty strings to None
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile if save_info checked
        profile = None
        username = getattr(intent.metadata, "username", "AnonymousUser")
        if username and username != "AnonymousUser":
            try:
                profile = UserProfile.objects.get(user__username=username)
            except UserProfile.DoesNotExist:
                profile = None

            if profile and save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = shipping_details.address.line1
                profile.default_street_address2 = shipping_details.address.line2
                profile.default_county = shipping_details.address.state
                profile.save()

        # Idempotency: check if order already exists (retry up to 5 times)
        order_exists = False
        attempt = 1
        query = self._order_exists_query(shipping_details, billing_details, grand_total, bag, pid)

        while attempt <= 5:
            try:
                Order.objects.get(**query)
                order_exists = True
                break
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200,
            )

        # Create the order + line items
        order = None
        try:
            order_kwargs = self._order_create_kwargs(shipping_details, billing_details, grand_total, bag, pid, profile)
            order = Order.objects.create(**order_kwargs)

            for item_id, item_data in json.loads(bag).items():
                product = Product.objects.get(id=item_id)
                if isinstance(item_data, int):
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                else:
                    for size, quantity in item_data.get("items_by_size", {}).items():
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                            product_size=size,
                        )

        except Exception as e:
            if order:
                # roll back partial order if something fails
                try:
                    order.delete()
                except Exception:
                    pass
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500,
            )

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe."""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )
