from django.shortcuts import render
from store.models import Store
from category.models import Category

def home(request):

    products = Store.objects.all().filter(is_available = True)
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'home.html', context)