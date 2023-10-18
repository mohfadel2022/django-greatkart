from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages

from store.models import Store, ReviewRating
from category.models import Category
from cart.models import CartItem

from cart.views import _get_cart_id
from order.models import OrderProduct

from .forms import ReviewForm

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

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(product_id = product.id, user=request.user)
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id = product.id, status=True)


    context = {
        'product': product,
        'in_cart': in_cart,
        'is_purchased': orderproduct,
        'reviews': reviews,
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

def submit_review(request, product_id):
        url = request.META.get('HTTP_REFERER')
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id= product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank You! Your review has been updates.')
            return redirect(url)


        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META['REMOTE_ADDR']
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank You! Your review has been submitted.')
                return redirect(url)
