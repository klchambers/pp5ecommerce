from django.shortcuts import render
from .models import Wine


# Create your views here.
def all_products(request):
    """View to return all products, including sorting and search"""

    products = Wine.objects.all()

    context = {
        'products': products
    }

    return render(request, 'products/products.html', context)
