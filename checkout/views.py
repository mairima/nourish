from decimal import Decimal
import json
import stripe

from django.conf import settings
from django.contrib import messages
from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .forms import OrderForm
from .models import Order, OrderLineItem, DiscountCode
from products.models import Product
from profiles.forms import ProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents
from newsletter.models import NewsletterSubscription


# ---------- Helpers ----------

def _bag_json(request):
    """Serialize current session bag to compact JSON string for metadata."""
    try:
        return json.dumps(
            request.session.get("bag", {}), separators=(",", ":")
        )
    except Exception:
        return "{}"


def _get_or_create_payment_intent(request, grand_total: Decimal):
    """
    Retrieve or create a Stripe PaymentIntent for this session.
    Returns client_secret or empty string if Stripe not configured.
    """
    stripe_public_key = getattr(settings, "STRIPE_PUBLIC_KEY", "")
    stripe_secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    stripe_currency = getattr(settings, "STRIPE_CURRENCY", "usd")

    if not (stripe_public_key and stripe_secret_key and grand_total > 0):
        return ""

    stripe.api_key = stripe_secret_key
    pi_id = request.session.get("pi_id")
    amount = int(Decimal(grand_total) * 100)
    metadata = {
        "username": (
            getattr(getattr(request, "user", None), "username", "")
            or "anonymous"
        ),
        "bag": _bag_json(request),
    }

    try:
        if pi_id:
            intent = stripe.PaymentIntent.retrieve(pi_id)
            if intent.status in {
                "requires_payment_method",
                "requires_confirmation",
                "requires_action",
                "processing",
            }:
                if intent.amount != amount:
                    intent = stripe.PaymentIntent.modify(
                        intent.id, amount=amount, metadata=metadata
                    )
                else:
                    stripe.PaymentIntent.modify(intent.id, metadata=metadata)
                return intent.client_secret

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=stripe_currency,
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
    """Send order confirmation email."""
    ctx = {"order": order}
    subject = render_to_string(
        "checkout/confirmation_emails/confirmation_email_subject.txt", ctx
    ).strip()
    body_txt = render_to_string(
        "checkout/confirmation_emails/confirmation_email_body.txt", ctx
    )
    send_mail(subject, body_txt, settings.DEFAULT_FROM_EMAIL, [order.email])


@require_POST
def cache_checkout_data(request):
    """Cache bag/save_info/username into the PaymentIntent metadata."""
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


# ---------- Main Checkout View ----------

@never_cache
@login_required
def checkout(request):
    """Handle checkout page logic, discount codes, and Stripe payment."""
    bag = request.session.get("bag", {})
    if not bag:
        messages.info(request, "Your checkout session has expired.")
        return redirect("products:products")

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        form_data = {
            key: request.POST[key]
            for key in [
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
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get("client_secret").split("_secret")[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            discount_percent = request.session.get("discount_percent", 0)
            order.save()

            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order, product=product, quantity=item_data
                        )
                    else:
                        for size, quantity in (
                            item_data["items_by_size"].items()
                        ):
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "A product in your bag was not found. "
                        "Please contact us for assistance.",
                    )
                    order.delete()
                    return redirect("bag:view_bag")

            # --- Apply discount if order >= €30 ---
            order_total = order.get_total()
            discount_applied = False

            if discount_percent:
                if order_total >= Decimal("30.00"):
                    order.grand_total = order_total - (
                        order_total * Decimal(discount_percent) / 100
                    )
                    order.discount_percent = discount_percent
                    discount_applied = True
                    order.save(
                        update_fields=["grand_total", "discount_percent"]
                    )
                    messages.success(
                        request,
                        f"A {discount_percent}% discount was applied 🎉",
                    )
                else:
                    order.grand_total = order_total
                    order.discount_percent = Decimal("0.00")
                    order.save(
                        update_fields=["grand_total", "discount_percent"]
                    )
                    messages.warning(
                        request,
                        "Discount cannot apply below €30. "
                        "You can use it next time.",
                    )
            else:
                order.grand_total = order_total
                order.save(update_fields=["grand_total"])

            if not discount_applied:
                request.session["discount_percent"] = discount_percent
            else:
                request.session.pop("discount_percent", None)

            request.session["save_info"] = "save-info" in request.POST
            request.session["bag"] = {}
            request.session.pop("discount_percent", None)

            return redirect(
                reverse("checkout:checkout_success", args=[order.order_number])
            )

        messages.error(request, "Please check your details and try again.")
    else:
        current_bag = bag_contents(request)
        total = current_bag["grand_total"]
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
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

    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing. "
            "Did you forget to set it in your environment?",
        )

    if "intent" not in locals():
        intent = _get_or_create_payment_intent(request, Decimal(0))

    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": (
            intent if isinstance(intent, str) else intent.client_secret
        ),
    }
    return render(request, "checkout/checkout.html", context)


# ---------- Apply Discount View ----------

def apply_discount(request):
    """Validate and apply a discount code."""
    if request.method == "POST":
        code = request.POST.get("discount_code", "").strip()
        try:
            discount = DiscountCode.objects.get(code__iexact=code, active=True)
            if discount.is_valid():
                request.session["discount_percent"] = discount.discount_percent
                messages.success(
                    request,
                    f"Discount code '{discount.code}' applied! "
                    f"{discount.discount_percent}% off your order.",
                )
            else:
                messages.warning(request, "This discount code has expired.")
        except DiscountCode.DoesNotExist:
            messages.error(request, "Invalid discount code.")
    return redirect("checkout:checkout")


# ---------- Checkout Success ----------

def checkout_success(request, order_number):
    """Handle successful checkouts."""
    save_info = request.session.get("save_info")
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        try:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            if order.user_profile_id != profile.id:
                order.user_profile = profile
                order.save(update_fields=["user_profile"])
        except Exception:
            pass

        if save_info:
            profile_data = {
                "default_phone_number": order.phone_number,
                "default_country": order.country,
                "default_postcode": order.postcode,
                "default_town_or_city": order.town_or_city,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_county": order.county,
            }
            user_profile_form = ProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(
        request,
        f"Order processed! Your order number is {order_number}. "
        f"A confirmation email will be sent to {order.email}.",
    )

    request.session.pop("bag", None)

    if not order.confirmation_sent:
        _send_order_confirmation(order)
        order.confirmation_sent = True
        order.save(update_fields=["confirmation_sent"])

    if order.discount_percent > 0:
        try:
            subscription = NewsletterSubscription.objects.get(
                email=order.email
            )
            subscription.discount_used = True
            subscription.save()
        except NewsletterSubscription.DoesNotExist:
            pass

    return render(request, "checkout/checkout_success.html", {"order": order})


@login_required
def order_history(request, order_number):
    """Display a user's past order details on the profile page."""
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(
        request,
        f"This is a past confirmation for order {order_number}. "
        "A confirmation email was sent at purchase time.",
    )

    context = {
        "order": order,
        "from_profile": True,
    }
    return render(request, "checkout/checkout_success.html", context)
