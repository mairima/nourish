from decimal import Decimal
import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
    reverse,
    HttpResponse,
)
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from bag.contexts import bag_contents
from newsletter.models import NewsletterSubscription
from products.models import Product
from profiles.forms import ProfileForm
from profiles.models import UserProfile

from .forms import OrderForm
from .models import Order, OrderLineItem, DiscountCode


# -------------------- Helpers --------------------

def _bag_json(request):
    """Serialize session bag into compact JSON."""
    try:
        return json.dumps(
            request.session.get("bag", {}),
            separators=(",", ":"),
        )
    except Exception:
        return "{}"


def _get_or_create_payment_intent(request, grand_total: Decimal):
    """Retrieve or create Stripe PaymentIntent."""
    pub_key = getattr(settings, "STRIPE_PUBLIC_KEY", "")
    sec_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    currency = getattr(settings, "STRIPE_CURRENCY", "usd")

    if not (pub_key and sec_key and grand_total > 0):
        return ""

    stripe.api_key = sec_key
    pi_id = request.session.get("pi_id")
    amount = int(grand_total * 100)

    metadata = {
        "username": getattr(request.user, "username", "") or "anonymous",
        "bag": _bag_json(request),
    }

    try:
        if pi_id:
            intent = stripe.PaymentIntent.retrieve(pi_id)
            valid_states = {
                "requires_payment_method",
                "requires_confirmation",
                "requires_action",
                "processing",
            }

            if intent.status in valid_states:
                if intent.amount != amount:
                    intent = stripe.PaymentIntent.modify(
                        intent.id,
                        amount=amount,
                        metadata=metadata,
                    )
                else:
                    stripe.PaymentIntent.modify(
                        intent.id,
                        metadata=metadata,
                    )
                return intent.client_secret

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={"enabled": True},
            metadata=metadata,
        )
        request.session["pi_id"] = intent.id
        return intent.client_secret

    except Exception as err:
        print(f"[Stripe] PaymentIntent error: {err}")
        request.session.pop("pi_id", None)
        return ""


def _send_order_confirmation(order):
    """Send confirmation email."""
    ctx = {"order": order}
    subject = render_to_string(
        "checkout/confirmation_emails/confirmation_email_subject.txt",
        ctx,
    ).strip()
    body_txt = render_to_string(
        "checkout/confirmation_emails/confirmation_email_body.txt",
        ctx,
    )

    send_mail(
        subject,
        body_txt,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )


# -------------------- Cache Data --------------------

@require_POST
def cache_checkout_data(request):
    """Cache metadata into PaymentIntent."""
    try:
        client_secret = request.POST.get("client_secret", "")
        if not client_secret or "_secret" not in client_secret:
            return HttpResponse("Invalid client_secret", status=400)

        pid = client_secret.split("_secret")[0]
        stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")

        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": _bag_json(request),
                "save_info": request.POST.get("save_info") or "",
                "username": (
                    getattr(request.user, "username", "") or "anonymous"
                ),
            },
        )
        return HttpResponse(status=200)

    except Exception as err:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now. "
            "Please try again later.",
        )
        return HttpResponse(content=str(err), status=400)


# -------------------- Checkout --------------------

@never_cache
@login_required
def checkout(request):
    """Handle checkout page, order creation, and Stripe."""
    bag = request.session.get("bag", {})
    if not bag:
        messages.info(request, "Your checkout session has expired.")
        return redirect("products:products")

    pub_key = settings.STRIPE_PUBLIC_KEY
    sec_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        fields = [
            "full_name",
            "email",
            "phone_number",
            "country",
            "postcode",
            "town_or_city",
            "street_address1",
            "street_address2",
            "county",
        ]
        form_data = {key: request.POST[key] for key in fields}

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)

            discount_percent = request.session.get("discount_percent", 0)
            order.save()

            # Save line items
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "A product in your bag was not found.",
                    )
                    order.delete()
                    return redirect("bag:view_bag")

                if isinstance(item_data, int):
                    OrderLineItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                else:
                    for size, qty in item_data["items_by_size"].items():
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=qty,
                            product_size=size,
                        )

            # Discount logic
            total = order.get_total()
            if discount_percent:
                if total >= Decimal("30.00"):
                    discount_amount = (
                        total * Decimal(discount_percent) / 100
                    )
                    order.grand_total = total - discount_amount
                    order.discount_percent = discount_percent
                    order.save(
                        update_fields=["grand_total", "discount_percent"],
                    )
                    messages.success(
                        request,
                        f"A {discount_percent}% discount was applied.",
                    )
                else:
                    order.grand_total = total
                    order.discount_percent = Decimal("0.00")
                    order.save(
                        update_fields=["grand_total", "discount_percent"],
                    )
                    messages.warning(
                        request,
                        "Discount cannot apply below €30.",
                    )
            else:
                order.grand_total = total
                order.save(update_fields=["grand_total"])

            request.session["save_info"] = (
                "save-info" in request.POST
            )
            request.session["bag"] = {}
            request.session.pop("discount_percent", None)

            return redirect(
                reverse("checkout:checkout_success",
                        args=[order.order_number])
            )

        messages.error(request, "Please check your details and try again.")

    else:
        ctx = bag_contents(request)
        total = ctx["grand_total"]

        stripe.api_key = sec_key
        intent = stripe.PaymentIntent.create(
            amount=round(total * 100),
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(
                    initial={
                        "full_name": profile.user.get_full_name(),
                        "email": profile.user.email,
                        "phone_number": profile.default_phone_number,
                        "country": profile.default_country,
                        "postcode": profile.default_postcode,
                        "town_or_city": profile.default_town_or_city,
                        "street_address1": profile.default_street_address1,
                        "street_address2": profile.default_street_address2,
                        "county": profile.default_county,
                    }
                )
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not pub_key:
        messages.warning(
            request,
            "Stripe public key is missing. "
            "Did you set it in your environment?",
        )

    if "intent" not in locals():
        intent = _get_or_create_payment_intent(request, Decimal(0))

    context = {
        "order_form": order_form,
        "stripe_public_key": pub_key,
        "client_secret": (
            intent if isinstance(intent, str) else intent.client_secret
        ),
    }
    return render(request, "checkout/checkout.html", context)


# -------------------- Discount Codes --------------------

def apply_discount(request):
    """Validate discount code and store percentage in session."""
    if request.method == "POST":
        code = request.POST.get("discount_code", "").strip()
        try:
            discount = DiscountCode.objects.get(
                code__iexact=code, active=True
            )
            if discount.is_valid():
                request.session["discount_percent"] = (
                    discount.discount_percent
                )
                messages.success(
                    request,
                    (
                        f"Discount code '{discount.code}' applied. "
                        f"{discount.discount_percent}% off."
                    ),
                )
            else:
                messages.warning(request, "This discount code expired.")
        except DiscountCode.DoesNotExist:
            messages.error(request, "Invalid discount code.")

    return redirect("checkout:checkout")


# -------------------- Checkout Success --------------------

def checkout_success(request, order_number):
    """Display success page and update profile + DB."""
    save_info = request.session.get("save_info")
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        try:
            profile, _ = UserProfile.objects.get_or_create(
                user=request.user
            )
            if order.user_profile_id != profile.id:
                order.user_profile = profile
                order.save(update_fields=["user_profile"])
        except Exception:
            pass

        if save_info:
            data = {
                "default_phone_number": order.phone_number,
                "default_country": order.country,
                "default_postcode": order.postcode,
                "default_town_or_city": order.town_or_city,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_county": order.county,
            }
            form = ProfileForm(data, instance=profile)
            if form.is_valid():
                form.save()

        from bag.models import UserCartItem
        UserCartItem.objects.filter(user=request.user).delete()

    request.session["bag"] = {}

    messages.success(
        request,
        (
            "Order processed! Your order number is "
            f"{order_number}. A confirmation email "
            f"will be sent to {order.email}."
        ),
    )

    if not order.confirmation_sent:
        _send_order_confirmation(order)
        order.confirmation_sent = True
        order.save(update_fields=["confirmation_sent"])

    if order.discount_percent > 0:
        try:
            sub = NewsletterSubscription.objects.get(email=order.email)
            sub.discount_used = True
            sub.save()
        except NewsletterSubscription.DoesNotExist:
            pass

    context = {"order": order}
    return render(request, "checkout/checkout_success.html", context)


# -------------------- Order History --------------------

@login_required
def order_history(request, order_number):
    """Display past orders inside profile page."""
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(
        request,
        (
            f"This is a past confirmation for order {order_number}. "
            "A confirmation email was sent at purchase time."
        ),
    )

    context = {
        "order": order,
        "from_profile": True,
    }
    return render(request, "checkout/checkout_success.html", context)
