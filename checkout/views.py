from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, 'Error: There is nothing in your bag!')
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Q0is82NHUwOmI7W26JwI0KQRsm5LdR4rKqIqNSssXMoAkvSHn0nqwUEJGtZp6cUQ7VRo0MNdtrx4b2BnKFDzKXL002PCsypDS',
        'client_secret': 'test_client_secrets',
    }

    return render(request, template, context)
