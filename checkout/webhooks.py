# checkout/webhooks.py
import json
import stripe
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import StripeWH_Handler


@csrf_exempt  # keep CSRF disabled for Stripe callbacks
@require_POST  # Stripe sends POST; safe to enforce
def webhook(request):
    """
    Stripe webhook endpoint.
    In dev, run:
      stripe listen --forward-to localhost:8000/checkout/wh/
    """
    stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")

    wh_secret = (
        getattr(settings, "STRIPE_WH_SECRET", "")
        or getattr(settings, "STRIPE_WEBHOOK_SECRET", "")
    )

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        if not wh_secret:
            # Fallback: accept unverified events (dev only)
            data = json.loads(payload.decode("utf-8"))
            event = stripe.Event.construct_from(data, stripe.api_key)
        else:
            event = stripe.Webhook.construct_event(
                payload=payload,
                sig_header=sig_header,
                secret=wh_secret,
            )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    handler = StripeWH_Handler(request)
    event_map = {
        "payment_intent.succeeded":
            handler.handle_payment_intent_succeeded,
        "payment_intent.payment_failed":
            handler.handle_payment_intent_payment_failed,
    }

    event_type = (
        event.get("type") if isinstance(event, dict) else event.type
    )
    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    return response
