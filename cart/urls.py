from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_item_cart/<int:product_id>/', views.decrease_item_cart, name='decrease_item_cart'),
    path('remove_item_cart/<int:product_id>/', views.remove_item_cart, name='remove_item_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
] 