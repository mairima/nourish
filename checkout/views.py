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
from .models import Order, OrderLineItem
from products.models import Product
from profiles.forms import ProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents


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


# ---------- Main views ----------
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

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
            order.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't "
                        "found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout:checkout_success',
                                    args=[order.order_number]))
        else:
            messages.error(request, ('There was an error with your form. '
                                     'Please double check your information.'))
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request,
                           "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Attempt to prefill the form with any info
        # the user maintains in their profile
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
        messages.warning(request, ('Stripe public key is missing. '
                                   'Did you forget to set it in '
                                   'your environment?'))

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

    # Send confirmation email
    _send_order_confirmation(order)

    return render(request, 'checkout/checkout_success.html', {'order': order})
