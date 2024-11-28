from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse # noqa
from django.contrib import messages
from products.models import Wine


# Create your views here.
def view_bag(request):
    """View to return shopping bag contents page"""
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Wine, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(
            request,
            f'Updated {product.friendly_name} quantity to {bag[item_id]}!')
    else:
        bag[item_id] = quantity
        messages.success(
            request,
            f'{product.friendly_name} added to shopping bag!')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ adjust a quantity of the specified product in the shopping bag """

    quantity = int(request.POST.get('quantity'))
    product = get_object_or_404(Wine, pk=item_id)

    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request,
            f"Updated {product.friendly_name} quantity to {bag[item_id]}")
    else:
        bag.pop(item_id)
        messages.success(
            request,
            f"Removed {product.friendly_name} quantity from {bag[item_id]}")

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    product = get_object_or_404(Wine, pk=item_id)
    try:
        bag = request.session.get('bag', {})

        bag.pop(item_id)
        messages.success(
            request, f"Removed {product.friendly_name} from your bag")

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(f"Error removing item: {e}")
        return HttpResponse(status=500)
