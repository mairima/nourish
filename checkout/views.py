# checkout/views.py
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

import stripe


def _create_payment_intent_if_possible(grand_total: Decimal) -> str:
    """
    Create and return a Stripe PaymentIntent client_secret if keys are present.
    Returns an empty string if it cannot create one.
    """
    stripe_public_key = getattr(settings, "STRIPE_PUBLIC_KEY", "")
    stripe_secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    stripe_currency = getattr(settings, "STRIPE_CURRENCY", "usd")

    if not (stripe_public_key and stripe_secret_key and grand_total and grand_total > 0):
        return ""

    try:
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=int(grand_total * 100),  # smallest currency unit
            currency=stripe_currency,
            automatic_payment_methods={"enabled": True},
        )
        return intent.client_secret
    except Exception as e:
        # Non-fatal: page can still render, just no payment confirmation.
        # Surface a warning during development.
        print(f"[Stripe] Failed to create PaymentIntent: {e}")
        return ""


def checkout(request):
    """
    GET:  render checkout with PaymentIntent client_secret, totals, and form.
    POST: validate form, create Order + LineItems, clear bag, redirect to success.
    """
    # 1) Require a non-empty bag
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse("products:products_index"))  # adjust if your URL name differs

    # 2) Totals from shared context helper
    totals = bag_contents(request)
    grand_total = Decimal(totals.get("grand_total") or 0)

    # 3) Hints if Stripe keys are missing (page still renders; client can’t confirm payment)
    stripe_public_key = getattr(settings, "STRIPE_PUBLIC_KEY", "")
    stripe_secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    if not stripe_public_key:
        messages.warning(request, "Stripe public key is missing. Did you set STRIPE_PUBLIC_KEY?")
    if not stripe_secret_key:
        messages.warning(request, "Stripe secret key is missing; payments are disabled.")

    # ----- POST: create order & redirect to success -----
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            try:
                # Save the order first (order_number assigned in model.save())
                order = order_form.save(commit=True)

                # Build line items from session bag structure
                for item_id, item_data in bag.items():
                    product = get_object_or_404(Product, pk=item_id)

                    # If item_data is an int: simple quantity (no sizes)
                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=int(item_data),
                        )
                    else:
                        # Expect: {"items_by_size": {"S": 1, "M": 2}} when sizes exist
                        items_by_size = item_data.get("items_by_size", {})
                        for size, quantity in items_by_size.items():
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                product_size=size,
                                quantity=int(quantity),
                            )

                # Clear bag after successful order creation
                request.session["bag"] = {}

                return redirect(reverse("checkout_success", args=[order.order_number]))
            except Exception as e:
                # Roll back and send user back to bag
                print(f"[Checkout] Error creating order: {e}")
                messages.error(
                    request,
                    "We couldn't process your order. Please try again, and contact us if the issue persists."
                )
                try:
                    if 'order' in locals() and isinstance(order, Order):
                        order.delete()
                except Exception:
                    pass
                return redirect(reverse("view_bag"))
        else:
            messages.error(request, "There was an error with your form. Please double-check your details.")
            # Fall through to render with errors and (re)create a PI

        # For POST with invalid form, create a fresh PaymentIntent to keep the page functional
        client_secret = _create_payment_intent_if_possible(grand_total)
        context = {
            "order_form": order_form,  # show field errors
            "stripe_public_key": stripe_public_key,
            "client_secret": client_secret or None,
            # Bag summary
            "bag_items": totals.get("bag_items"),
            "total": totals.get("total"),
            "delivery": totals.get("delivery"),
            "grand_total": grand_total,
            "product_count": totals.get("product_count"),
            "free_delivery_delta": totals.get("free_delivery_delta"),
        }
        return render(request, "checkout/checkout.html", context)

    # ----- GET: create a PaymentIntent & render -----
    order_form = OrderForm()
    client_secret = _create_payment_intent_if_possible(grand_total)

    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": client_secret or None,
        # Bag summary
        "bag_items": totals.get("bag_items"),
        "total": totals.get("total"),
        "delivery": totals.get("delivery"),
        "grand_total": grand_total,
        "product_count": totals.get("product_count"),
        "free_delivery_delta": totals.get("free_delivery_delta"),
    }
    return render(request, "checkout/checkout.html", context)


def checkout_success(request, order_number):
    """
    Simple success page after order creation & payment confirmation.
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f"Order successfully processed! Your order number is {order_number}.")
    return render(request, "checkout/checkout_success.html", {"order": order})
