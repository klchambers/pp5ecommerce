from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Wine, Category, Region


# Create your views here.
def all_products(request):
    """View to return all products, including sorting, filtering, and search"""

    products = Wine.objects.all()
    query = None
    categories = Category.objects.all()
    region = Region.objects.all()

    # Initialise lists for filters
    selected_categories = []
    selected_regions = []

    if request.GET:
        # Search term query
        if 'q' in request.GET:
            query = request.GET.get('q')
            if query:
                queries = Q(name__icontains=query) | Q(description__icontains=query) # noqa
                products = products.filter(queries)
            else:
                messages.error(request,
                               'Error: You did not enter a search term')
                return redirect(reverse('products'))

        # Category filter query
        if 'category' in request.GET:
            selected_categories = request.GET.getlist('category')
            if selected_categories:
                products = products.filter(
                    category__id__in=selected_categories)
        else:
            selected_categories = []

        # Region filter query
        if 'region' in request.GET:
            selected_regions = request.GET.getlist('region')
            if selected_regions:
                products = products.filter(region__id__in=selected_regions)
        else:
            selected_regions = []

        """Sorting logic adapted from code posted by
        Stack Overflow user Prakhar on 31/7/2021
        https://stackoverflow.com/questions/68604759/how-to-sort-product-by-price-low-to-high-and-high-to-low-in-django-with-fillters""" # noqa
        sort_by = request.GET.get("sort", "l2h")
        if sort_by == "l2h":
            products = products.order_by("price")
        elif sort_by == "h2l":
            products = products.order_by("-price")

    context = {
        'products': products,
        'search_term': query,
        'categories': categories,
        'regions': region,
        'selected_categories': selected_categories,
        'selected_regions': selected_regions,
    }

    return render(request, 'products/products.html', context)


def product_info(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Wine, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_info.html', context)
