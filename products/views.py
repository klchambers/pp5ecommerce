from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Wine, Category, Region
from .forms import ProductForm


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


@login_required
def add_product(request):
    """
    Add a product to the store
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only superadmin can do that!')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_info', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. \
                           Please ensure that the form is valid')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only superadmin can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Wine, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_info', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. \
                           Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """Delete a product from the store"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only superadmin can do that!')
        return redirect(reverse('home'))

    product = get_object_or_404(Wine, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
