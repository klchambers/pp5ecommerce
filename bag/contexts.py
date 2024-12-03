from decimal import Decimal
from django.conf import settings
from django.contrib import messages
from products.models import Wine


def bag_contents(request):
    """
    Retreives and calculates contents of the user's shopping
    bag from the session

    If an item is no longer available (i.e. it has been deleted from the store)
    then pop it from the bag and display an informative message to the user
    """
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, quantity in list(bag.items()):
        try:
            product = Wine.objects.get(pk=item_id)
            total += quantity * product.price
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
            })
        except Wine.DoesNotExist:
            bag.pop(item_id)
            messages.error(request, f'product with ID {item_id} was removed \
                from the bag as this product no longer exists')

    delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
    grand_total = delivery + total
    request.session['bag'] = bag

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'grand_total': grand_total,
    }

    return context
