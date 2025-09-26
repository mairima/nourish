# checkout/webhooks.py
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

import json
import stripe


@require_POST
@csrf_exempt
def webhook(request):
    """
    Basic Stripe webhook endpoint.

    In dev, run:
      stripe listen --forward-to localhost:8000/checkout/wh/

    Expects STRIPE_WH_SECRET (or STRIPE_WEBHOOK_SECRET) and STRIPE_SECRET_KEY
    in your settings / environment.
    """
    # Configure Stripe
    stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")
    # Support either env var name
    wh_secret = (
        getattr(settings, "STRIPE_WH_SECRET", "")
        or getattr(settings, "STRIPE_WEBHOOK_SECRET", "")
    )

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    # Verify the event with the webhook signing secret (recommended)
    if wh_secret:
        try:
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
    else:
        # Fallback: accept unverified events (NOT recommended for production)
        try:
            data = json.loads(payload.decode("utf-8"))
            event = stripe.Event.construct_from(data, stripe.api_key)
        except Exception:
            return HttpResponse(status=400)

    # ---- Handle a few example events ----
    etype = getattr(event, "type", None) or event.get("type")
    data_object = (
        event.data.object if hasattr(event, "data") else event.get("data", {}).get("object", {})
    )

    if etype == "payment_intent.succeeded":
        # e.g. mark order paid using metadata, send emails, etc.
        # pi_id = data_object.get("id")
        pass

    elif etype == "payment_intent.payment_failed":
        # log / notify as needed
        pass

    # Always return 200 to acknowledge receipt
    return HttpResponse(status=200)
