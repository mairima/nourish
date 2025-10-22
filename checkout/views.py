# checkout/views.py
from decimal import Decimal
import json
import stripe

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from profiles.forms import ProfileForm   # ← use ProfileForm instead of UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents


def _bag_json(request):
    """Serialize the current session bag to a compact JSON string for metadata."""
    try:
        return json.dumps(request.session.get("bag", {}), separators=(",", ":"))
    except Exception:
        return "{}"


def _get_or_create_payment_intent(request, grand_total: Decimal):
    """
    Retrieve an existing PI from the session or create a new one.
    Returns a client_secret (string) or "" if Stripe is not configured.
    """
    stripe_public_key = getattr(settings, "STRIPE_PUBLIC_KEY", "")
    stripe_secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    stripe_currency = getattr(settings, "STRIPE_CURRENCY", "usd")

    if not (stripe_public_key and stripe_secret_key and grand_total and grand_total > 0):
        return ""

    stripe.api_key = stripe_secret_key

    pi_id = request.session.get("pi_id")
    amount = int(Decimal(grand_total) * 100)

    metadata = {
        "username": getattr(getattr(request, "user", None), "username", "") or "anonymous",
        "bag": _bag_json(request),
    }

    try:
        if pi_id:
            intent = stripe.PaymentIntent.retrieve(pi_id)
            if intent.status in {"requires_payment_method", "requires_confirmation", "requires_action", "processing"}:
                if intent.amount != amount:
                    intent = stripe.PaymentIntent.modify(intent.id, amount=amount, metadata=metadata)
                else:
                    stripe.PaymentIntent.modify(intent.id, metadata=metadata)
                return intent.client_secret
            # else: succeeded/canceled → fall through to create new

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=stripe_currency,
            automatic_payment_methods={"enabled": True},
            metadata=metadata,
        )
        request.session["pi_id"] = intent.id
        return intent.client_secret

    except Exception as e:
        print(f"[Stripe] PaymentIntent error: {e}")
        request.session.pop("pi_id", None)
        return ""


def checkout(request):
    """
    GET: render checkout with PI client_secret, totals, and form.
    POST: validate form, create Order + LineItems, clear bag, redirect to success.
    """
    bag = request.session.get("bag", {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment.")
        return redirect(reverse("products:products_index"))  # adjust if your products index name differs

    totals = bag_contents(request)
    grand_total = Decimal(totals.get("grand_total") or 0)

    stripe_public_key = getattr(settings, "STRIPE_PUBLIC_KEY", "")
    stripe_secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    if not stripe_public_key:
        messages.warning(request, "Stripe public key is missing. Did you set STRIPE_PUBLIC_KEY?")
    if not stripe_secret_key:
        messages.warning(request, "Stripe secret key is missing; payments are disabled.")

    if request.method == "POST":
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            try:
                # Create the order
                order = order_form.save(commit=True)

                # (Optional) Attach profile immediately so FK exists before redirect
                if request.user.is_authenticated and not order.user_profile_id:
                    try:
                        profile, _ = UserProfile.objects.get_or_create(user=request.user)
                        order.user_profile = profile
                        order.save(update_fields=["user_profile"])
                    except Exception:
                        # don't block checkout if linkage fails
                        pass

                # Create line items from bag
                for item_id, item_data in bag.items():
                    product = get_object_or_404(Product, pk=item_id)

                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order, product=product, quantity=int(item_data)
                        )
                    else:
                        for size, quantity in item_data.get("items_by_size", {}).items():
                            OrderLineItem.objects.create(
                                order=order, product=product, product_size=size, quantity=int(quantity)
                            )

                # Clear bag & cached PI
                request.session["bag"] = {}
                request.session.pop("pi_id", None)

                return redirect(reverse("checkout_success", args=[order.order_number]))

            except Exception as e:
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

        # POST with invalid form: ensure a PI exists
        client_secret = _get_or_create_payment_intent(request, grand_total)
        return render(
            request,
            "checkout/checkout.html",
            {
                "order_form": order_form,
                "stripe_public_key": stripe_public_key,
                "client_secret": client_secret or None,
                "bag_items": totals.get("bag_items"),
                "total": totals.get("total"),
                "delivery": totals.get("delivery"),
                "grand_total": grand_total,
                "product_count": totals.get("product_count"),
                "free_delivery_delta": totals.get("free_delivery_delta"),
            },
        )

    # GET
    order_form = OrderForm()
    client_secret = _get_or_create_payment_intent(request, grand_total)
    return render(
        request,
        "checkout/checkout.html",
        {
            "order_form": order_form,
            "stripe_public_key": stripe_public_key,
            "client_secret": client_secret or None,
            "bag_items": totals.get("bag_items"),
            "total": totals.get("total"),
            "delivery": totals.get("delivery"),
            "grand_total": grand_total,
            "product_count": totals.get("product_count"),
            "free_delivery_delta": totals.get("free_delivery_delta"),
        },
    )


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # Attach the order to the logged-in user's profile (idempotent)
    if request.user.is_authenticated:
        try:
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            if order.user_profile_id != profile.id:
                order.user_profile = profile
                order.save(update_fields=["user_profile"])
        except Exception:
            # Don't break success page if something goes wrong
            pass

        # Optionally persist address info to the profile
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            # ← use ProfileForm here (you don't have UserProfileForm)
            user_profile_form = ProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(
        request,
        f'Order successfully processed! Your order number is {order_number}. '
        f'A confirmation email will be sent to {order.email}.'
    )

    # Clear the bag
    request.session.pop('bag', None)

    return render(request, 'checkout/checkout_success.html', {'order': order})
