from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import stripe
import logging

from checkout.webhook_handler import StripeWH_Handler

# Setup logger
logger = logging.getLogger(__name__)


@require_POST
@csrf_exempt
def webhook(request):
    """Listen for webhooks from Stripe"""
    # Setup
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Get the webhook data and verify its signature
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    event = None

    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, wh_secret
        )
        logger.info(f"Received Stripe event: {event['type']}")
    except ValueError as e:
        # Invalid payload
        logger.error(f"Invalid payload received from Stripe: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        logger.error(f"Invalid signature from Stripe: {e}")
        return HttpResponse(status=400)
    except Exception as e:
        # Any other errors
        logger.error(f"Error while handling Stripe webhook: {e}")
        return HttpResponse(content=str(e), status=400)

    # Set up a webhook handler
    handler = StripeWH_Handler(request)

    # Map webhook events to relevant handler functions
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed, # noqa
    }

    # Get the webhook type from Stripe
    event_type = event.get('type', 'unknown_event')

    # Get the event handler if available, otherwise use a generic handler
    event_handler = event_map.get(event_type, handler.handle_event)

    # Call the event handler with the event
    try:
        response = event_handler(event)
        logger.info(f"Webhook {event_type} handled successfully")
        return response
    except Exception as e:
        logger.error(f"Error handling {event_type}: {e}")
        return HttpResponse(
            content=f"Error handling {event_type}: {e}", status=500)
