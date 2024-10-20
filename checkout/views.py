from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem # noqa
from products.models import Wine
from bag.contexts import bag_contents
from decimal import Decimal

import stripe


def calculate_delivery_cost(order_total):
    """
    Calculate the delivery cost based on the order total
    using the STANDARD_DELIVERY_PERCENTAGE from settings.
    """
    # Ensure order_total is a Decimal
    if isinstance(order_total, float):
        order_total = Decimal(order_total)

    if order_total <= 0:
        return Decimal(0)

    # Convert STANDARD_DELIVERY_PERCENTAGE to Decimal
    delivery_percentage = Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal(100) # noqa
    return delivery_percentage * order_total


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
            order = order_form.save()

            # Calculate subtotal from the bag
            subtotal = 0
            for item_id, quantity in bag.items():
                try:
                    product = Wine.objects.get(id=item_id)
                    # Sum the total price for each product
                    subtotal += product.price * quantity
                except Wine.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found."
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            # Calculate delivery cost and update order
            order.delivery_cost = calculate_delivery_cost(subtotal)
            order.save()  # Save the order after setting the delivery cost

            # Add line items to the order
            for item_id, item_data in bag.items():
                product = Wine.objects.get(id=item_id)
                order_line_item = OrderLineItem(
                    order=order,
                    product=product,
                    quantity=item_data,
                )
                order_line_item.save()

            order.update_total()

            request.session['save_info'] = 'save-info' in request.POST
            print(f"Order Number: {order.order_number}")
            return redirect(
                reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
            current_bag = bag_contents(request)
            total = current_bag['grand_total']
            stripe_total = round(total * 100)
            stripe.api_key = stripe_secret_key
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY
            )

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, 'Error: There is nothing in your bag!')
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY
        )

        order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request,
                         'No public key set! \
                        Did you forget to set it in your environment?')

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
    save_info = request.session.get('save_info') # noqa
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
