from django.contrib import admin
from .models import Payment, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ['payment', 'user', 'product', 'product_price', 'quantity', 'is_ordered', 'created_at', 'updated_at']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'total', 'tax', 'status', 'is_ordered', 'created_at' ]
    list_filter =['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'product', 'product_price', 'quantity', 'is_ordered', 'created_at', 'updated_at']
    list_filter =['updated_at', 'is_ordered']
    search_fields = ['order', 'product']
    list_per_page = 20

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at']



admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
