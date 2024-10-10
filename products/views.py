from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Wine


# Create your views here.
def all_products(request):
    """View to return all products, including sorting and search"""

    products = Wine.objects.all()
    query = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               'Error: You did not enter a search term')
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query) # noqa

            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)
