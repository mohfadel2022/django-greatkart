from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgotPassword/', views.forgot_password, name='forgotPassword'),
    path('resetPassword/', views.reset_password, name='resetPassword'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset_password_validation/<uidb64>/<token>/', views.reset_password_validation, name='reset_password_validation'),
    
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<order_id>/', views.order_detail, name='order_detail'),



    
]