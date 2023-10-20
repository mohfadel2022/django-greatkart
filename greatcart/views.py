from django.shortcuts import render
from store.models import Store, ReviewRating
from category.models import Category

def home(request):

    products = Store.objects.all().filter(is_available = True).order_by('created_date')

    # Get the Product Reviews
    for product in products:
        reviews = ReviewRating.objects.filter(product_id = product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews
    }
    return render(request, 'home.html', context)