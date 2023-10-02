from .models import Category

def categories_links(request):
    links = Category.objects.all()

    return dict(cat_links=links)
