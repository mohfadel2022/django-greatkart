from .models import Cart, CartItem

from itertools import chain

from .views import _get_cart_id

def cart_counter(request):
    cart_count = 0
    cart_items = {}
    if 'admin' in request.path:
        return ()
    else:
        try:
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
                # for cart in carts:
                #     cart_items = list(chain(cart_items, CartItem.objects.filter(cart = cart)))
            else:
                cart = Cart.objects.filter(cart_id = _get_cart_id(request))
                cart_items = CartItem.objects.all().filter(cart = cart[:1])
            
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    
    return dict(cart_counter = cart_count)