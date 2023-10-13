from django.contrib import admin
from .models import Store, Variation

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}
    list_display = ('id', 'product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(Store, ProductAdmin)
admin.site.register(Variation, VariationAdmin)