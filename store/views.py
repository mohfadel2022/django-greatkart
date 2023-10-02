from django.shortcuts import render, get_object_or_404
from store.models import Store
from category.models import Category


# Create your views here.

def store(request, category_slug = None):

    category = category_slug
    products = None
    products_count = 0

    if category_slug != None :
        category = get_object_or_404(Category, slug = category_slug)
        products = Store.objects.filter(category=category, is_available = True)
        products_count = products.count()

    else:
        products = Store.objects.all().filter(is_available = True)
        products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):

    try:
        product = Store.objects.get(category__slug = category_slug, slug = product_slug)
    except Exception as e:
        raise e

    context = {
        'product': product,
    }

    return render(request, 'store/product_detail.html', context)