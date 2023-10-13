from django.db import models
from store.models import Store, Variation
from account.models import Account

class Cart(models.Model):
    cart_id     = models.CharField(max_length=50, blank=True)
    date_added  = models.DateField(auto_now_add=True)
    user        = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)


    def __str__(self) -> str:
        return self.cart_id
    
class CartItem(models.Model):
    product     = models.ForeignKey(Store, on_delete=models.CASCADE)
    # variation   = models.ManyToManyField(Variation, blank=True)
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity    = models.IntegerField()
    images      = models.ImageField(upload_to='photos/products', blank=True)
    is_active   = models.BooleanField(default=True)
    user        = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __sunicode__(self) -> str:
        return self.product