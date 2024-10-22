from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, OrderLineItem
from products.models import Wine
from profiles.models import UserProfile
import logging
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the confirmation email to the user"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )
        try:
            send_mail(
                subject.strip(),
                body,
                settings.DEFAULT_FROM_EMAIL,
                [cust_email],
            )
        except Exception as e:
            logging.error(f"Error sending confirmation email: {e}")
            raise

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        logging.info(f"Unhandled event: {event['type']}")
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        try:
            intent = event.data.object
            pid = intent.id
            metadata = intent.metadata

            # Ensure metadata fields exist
            if not metadata or not all(k in metadata for k in ('bag', 'save_info', 'username')):
                logging.error("Missing metadata in payment intent")
                return HttpResponse(content=f"Webhook received: {event['type']} | ERROR: Missing metadata", status=500)

            bag = metadata['bag']
            save_info = metadata['save_info']
            username = metadata['username']

            # Convert bag to JSON object
            bag_data = json.loads(bag)
            logging.info(f"Processing payment for {username}. Bag: {bag_data}")

            billing_details = intent.charges.data[0].billing_details
            shipping_details = intent.shipping
            grand_total = round(intent.charges.data[0].amount / 100, 2)

            # Clean shipping details
            for field, value in shipping_details.address.items():
                if value == "":
                    shipping_details.address[field] = None

            # Handle profile if user is not Anonymous
            profile = None
            if username != 'AnonymousUser':
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_phone_number = shipping_details.phone
                    profile.default_country = shipping_details.address.country
                    profile.default_postcode = shipping_details.address.postal_code
                    profile.default_town_or_city = shipping_details.address.city
                    profile.default_street_address1 = shipping_details.address.line1
                    profile.default_street_address2 = shipping_details.address.line2
                    profile.default_county = shipping_details.address.state
                    profile.save()

            # Check if order already exists
            order_exists = False
            attempt = 1
            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        full_name__iexact=shipping_details.name,
                        email__iexact=billing_details.email,
                        phone_number__iexact=shipping_details.phone,
                        country__iexact=shipping_details.address.country,
                        postcode__iexact=shipping_details.address.postal_code,
                        town_or_city__iexact=shipping_details.address.city,
                        street_address1__iexact=shipping_details.address.line1,
                        street_address2__iexact=shipping_details.address.line2,
                        county__iexact=shipping_details.address.state,
                        grand_total=grand_total,
                        original_bag=bag,
                        stripe_pid=pid,
                    )
                    order_exists = True
                    logging.info(f"Order {order.order_number} already exists")
                    break
                except Order.DoesNotExist:
                    attempt += 1
                    time.sleep(1)

            # If order exists, send confirmation email
            if order_exists:
                self._send_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                    status=200
                )

            # If order doesn't exist, create it
            else:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                    grand_total=grand_total,
                )

                # Add line items to the order
                for item_id, item_data in bag_data.items():
                    try:
                        product = Wine.objects.get(id=item_id)
                    except Wine.DoesNotExist:
                        logging.error(f"Product with ID {item_id} does not exist.")
                        order.delete()
                        return HttpResponse(content=f"Webhook received: {event['type']} | ERROR: Product not found", status=500)

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

                logging.info(f"Order {order.order_number} created successfully")

                # Send confirmation email
                self._send_confirmation_email(order)

                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
                    status=200
                )

        except Exception as e:
            logging.error(f"Error in handle_payment_intent_succeeded: {e}")
            return HttpResponse(content=f"Webhook received: {event['type']} | ERROR: {str(e)}", status=500)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        logging.info(f"Payment failed for event {event['type']}")
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
