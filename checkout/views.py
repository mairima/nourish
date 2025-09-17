# checkout/views.py
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse

from .forms import OrderForm
from bag.contexts import bag_contents

# Optional import so the view still works if stripe isn't installed
try:
    import stripe  # type: ignore
except Exception:  # pragma: no cover
    stripe = None


def checkout(request):
    """
    Render the checkout page.
    - Redirects if the bag is empty.
    - Creates a Stripe PaymentIntent (when keys exist) and exposes its client_secret.
    """
    # 1) Require a non-empty bag
    if not request.session.get("bag"):
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse("products:products_index"))  # adjust if your list view name differs

    # 2) Totals & items from shared context helper
    totals = bag_contents(request)
    grand_total = totals.get("grand_total") or Decimal("0.00")

    # 3) Stripe config
    stripe_public_key = getattr(settings, "STRIPE_PUBLIC_KEY", "")
    stripe_secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    stripe_currency = getattr(settings, "STRIPE_CURRENCY", "usd")

    client_secret = None

    # 4) Create a PaymentIntent when possible (needed to actually confirm a payment)
    if stripe and stripe_public_key and stripe_secret_key and grand_total > 0:
        try:
            stripe.api_key = stripe_secret_key
            amount_cents = int(Decimal(grand_total) * 100)  # smallest currency unit
            intent = stripe.PaymentIntent.create(
                amount=amount_cents,
                currency=stripe_currency,
            )
            client_secret = intent.client_secret
        except Exception as e:
            messages.warning(
                request,
                "We couldn't initialize the payment session. You can still fill the form, "
                f"but payment confirmation may fail: {e}"
            )
    else:
        # Helpful hints if keys are missing
        if not stripe_public_key:
            messages.warning(request, "Stripe public key is missing; card field cannot be initialised.")
        if not stripe_secret_key:
            messages.warning(request, "Stripe secret key is missing; payments are disabled.")

    # 5) Render form
    order_form = OrderForm()
    context = {
        "order_form": order_form,
        # Stripe data consumed by checkout.js
        "stripe_public_key": stripe_public_key,
        "client_secret": client_secret,
        # Bag summary
        "bag_items": totals.get("bag_items"),
        "total": totals.get("total"),
        "delivery": totals.get("delivery"),
        "grand_total": grand_total,
        "product_count": totals.get("product_count"),
        "free_delivery_delta": totals.get("free_delivery_delta"),
    }
    return render(request, "checkout/checkout.html", context)
