# checkout/views.py
from decimal import Decimal
import json
import stripe

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST

from django.core.mail import send_mail
from django.template.loader import render_to_string

from .forms import OrderForm
from .models import Order, OrderLineItem, DiscountCode
from products.models import Product
from profiles.forms import ProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents
# Import the newsletter subscription model and timezone utilities
from newsletter.models import NewsletterSubscription
from django.utils import timezone

# ---------- Helpers ----------

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
            if intent.status in {
                "requires_payment_method", "requires_confirmation",
                "requires_action", "processing"
            }:
                if intent.amount != amount:
                    intent = stripe.PaymentIntent.modify(intent.id, amount=amount, metadata=metadata)
                else:
                    stripe.PaymentIntent.modify(intent.id, metadata=metadata)
                return intent.client_secret
            # else: succeeded/canceled → create a fresh one

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


# in checkout/views.py

def _send_order_confirmation(order):
    """Send order confirmation email using your subject/body templates."""
    ctx = {"order": order}
    subject = render_to_string(
        "checkout/confirmation_emails/confirmation_email_subject.txt", ctx
    ).strip()  # keep subject on one line
    body_txt = render_to_string(
        "checkout/confirmation_emails/confirmation_email_body.txt", ctx
    )

    send_mail(
        subject,
        body_txt,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )


# ---------- Re-added from v1: cache pre-checkout metadata ----------

@require_POST
def cache_checkout_data(request):
    """
    Caches bag/save_info/username into the existing PaymentIntent metadata.
    Matches the flow used by Code Institute's stripe_elements.js.
    """
    try:
        client_secret = request.POST.get("client_secret", "")
        if not client_secret or "_secret" not in client_secret:
            return HttpResponse("Invalid client_secret", status=400)

        pid = client_secret.split("_secret")[0]
        stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")

        stripe.PaymentIntent.modify(pid, metadata={
            "bag": _bag_json(request),
            "save_info": request.POST.get("save_info") or "",
            "username": getattr(request.user, "username", "") or "anonymous",
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, "Sorry, your payment cannot be processed right now. Please try again later.")
        return HttpResponse(content=str(e), status=400)


# ---------- Main checkout view ----------
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def checkout(request):
    """Handle checkout page logic, including discount codes and Stripe payment."""
    bag = request.session.get('bag', {})
    if not bag:
        messages.info(request, "Your checkout session has expired.")
        return redirect('products:products')

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)

            # --- Discount code logic ---
            discount_code = request.POST.get("discount_code", "").strip()
            discount_percent = 0
            if discount_code:
                try:
                    code = DiscountCode.objects.get(code__iexact=discount_code)
                    if code.is_valid():
                        discount_percent = code.discount_percent
                        messages.success(
                            request,
                            f"Discount code '{discount_code}' applied: "
                            f"{discount_percent}% off your total."
                        )
                        # Mark as used if one-time
                        if code.one_time_use:
                            code.active = False
                            code.save()
                    else:
                        messages.error(request, "That discount code has expired.")
                except DiscountCode.DoesNotExist:
                    messages.error(request, "Invalid discount code entered.")
            # --- End discount code logic ---

            # Create order and items
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        "One of the products in your bag wasn't found. "
                        "Please contact us for assistance."
                    )
                    order.delete()
                    return redirect('bag:view_bag')

            # Apply discount to total
            if discount_percent > 0:
                order_total = order.get_total()
                order.grand_total = order_total - (order_total * discount_percent / 100)
                order.discount_percent = discount_percent
                order.save(update_fields=["grand_total", "discount_percent"])

            request.session['save_info'] = 'save-info' in request.POST
            request.session['bag'] = {}
            return redirect(reverse('checkout:checkout_success', args=[order.order_number]))
        else:
            messages.error(request, "Please check your details and try again.")
    else:
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(
            request,
            'Stripe public key is missing. '
            'Did you forget to set it in your environment?'
        )

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


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

   # Send confirmation email only once per order
    if not order.confirmation_sent:
        _send_order_confirmation(order)
        order.confirmation_sent = True
        order.save(update_fields=["confirmation_sent"])
        # ^ Ensures no duplicate email if page is refreshed

    return render(request, 'checkout/checkout_success.html', {'order': order})

# Import the newsletter subscription model and timezone utilities
def apply_discount(request, order_total, email, discount_code):
    try:
        sub = NewsletterSubscription.objects.get(email=email)
        if sub.discount_code == discount_code and sub.discount_valid():
            discounted_total = order_total * 0.9  # 10% off
            sub.mark_discount_used()  # mark as used
            return discounted_total
    except NewsletterSubscription.DoesNotExist:
        pass
    return order_total