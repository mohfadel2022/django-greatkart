from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Store
from cart.models import Cart, CartItem

def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    product = Store.objects.get(id=product_id) # Get a product
    try:
        cart = Cart.objects.get(cart_id = _get_cart_id(request)) # Get a cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _get_cart_id(request)
        )
    cart.save()

    try:        
        cart_item =  CartItem.objects.get(product = product, cart = cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        cart_item.save()

    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _get_cart_id(request))
    product = get_object_or_404(Store, id = product_id) 
    # product = Store.objects.filter(id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_item_cart(request, product_id):
    cart = Cart.objects.get(cart_id = _get_cart_id(request))
    product = get_object_or_404(Store, id = product_id)
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()

    return redirect('cart')

def cart(request, total=0, quantity=0, tax= 0, cart_item=None):

    try:
        cart = Cart.objects.get(cart_id = _get_cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart, is_active = True)

        for cart_item in cart_items:
            quantity += cart_item.quantity
            total += cart_item.quantity * cart_item.product.price
        tax = (2 * total)/ 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items': cart_items
    }
    
    return render(request, 'store/cart.html', context)