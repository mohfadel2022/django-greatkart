from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

from store.models import Store
from category.models import Category
from cart.models import CartItem

from cart.views import _get_cart_id

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

    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'products': paged_products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):

    try:
        product = Store.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _get_cart_id(request), product = product).exists()
    except Exception as e:
        raise e

    context = {
        'product': product,
        'in_cart': in_cart
    }

    return render(request, 'store/product_detail.html', context)

def search(request):
    

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            products = Store.objects.order_by('-created_date').filter(Q(description__icontains=keywords) | Q(product_name__icontains=keywords))
            products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count
    }

    return render(request, 'store/store.html', context)
