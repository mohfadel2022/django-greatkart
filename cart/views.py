from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Store
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required

from itertools import chain

from account.models import Account


def _get_cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart1(request, product_id):

    product = Store.objects.get(id=product_id) # Get a product
    try:
        cart = Cart.objects.get(cart_id = _get_cart_id(request)) # Get a cart

    except Cart.DoesNotExist:

        cart = Cart.objects.create(
            cart_id = _get_cart_id(request)
        )
        if request.user.is_authenticated:
            cart.user = request.user
        else:
            pass
    
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


def add_to_cart(request, product_id):

    # cart_items = {}
    product = Store.objects.get(id=product_id) # Get a product
    # cart = Cart.objects.get(cart_id = _get_cart_id(request))

    if request.user.is_authenticated:

        # User's Cart existing
        try:
            cart = Cart.objects.get(user = request.user)
            cart = cart
            try:
                cart_item = CartItem.objects.get(product=product, user=request.user)
                cart_item.quantity += 1
                cart_item.save()       
                
            except CartItem.DoesNotExist:                
                cart_item = CartItem.objects.create(
                    product = product,
                    cart = cart,
                    user = request.user,
                    quantity = 1
                )
                cart_item.save()    
        # Create New user's Cart 
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _get_cart_id(request))
            cart.user = request.user
            cart.save()
            try:
                cart_item = CartItem.objects.all().get(product=product, cart = cart)
                cart_item.quantity += 1
                cart_item.user = request.user
                cart_item.save()       
                
            except CartItem.DoesNotExist:
                
                cart_item = CartItem.objects.create(
                    product = product,
                    cart = cart,
                    user = request.user,
                    quantity = 1
                )
                cart_item.save()     

            
    else:
        try:
            cart = Cart.objects.get(cart_id = _get_cart_id(request))
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                cart_item.quantity += 1    
                cart_item.save()

            except CartItem.DoesNotExist:    
                cart_item = CartItem.objects.create(
                            product = product,
                            cart = cart,
                            quantity = 1
                            )
                cart_item.save()       
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _get_cart_id(request))
            cart.save()
            cart_item = CartItem.objects.create(
                        product = product,
                        cart = cart,
                        quantity = 1
                        )
            cart_item.save()  

    return redirect('cart')

def decrease_item_cart(request, product_id):

    product = get_object_or_404(Store, id = product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.all().filter(user=request.user)        
        for cart in carts:
            try:
                cart_item = CartItem.objects.get(product = product, cart = cart)
            except CartItem.DoesNotExist:
                pass
    else:
        cart = Cart.objects.get(cart_id = _get_cart_id(request))
        cart_item = CartItem.objects.get(product = product, cart = cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')
    
def decrease_item_cart1(request, product_id):

    cart = Cart.objects.get(cart_id = _get_cart_id(request))
    product = get_object_or_404(Store, id = product_id) 
    cart_item = CartItem.objects.get(product = product, cart = cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

def remove_item_cart1(request, product_id):

    product = get_object_or_404(Store, id = product_id)
    

    cart = Cart.objects.get(cart_id = _get_cart_id(request))
    cart_item = CartItem.objects.get(product = product, cart = cart)
    cart_item.delete()

    return redirect('cart')
def remove_item_cart(request, product_id):

    product = get_object_or_404(Store, id = product_id)
    
    cart_item = None
    if request.user.is_authenticated:
        carts = Cart.objects.all().filter(user=request.user)        
        for cart in carts:
            try:
                cart_item = CartItem.objects.filter(product = product, cart = cart)
            except CartItem.DoesNotExist:
                pass
    else:
        cart = Cart.objects.get(cart_id = _get_cart_id(request))
        cart_item = CartItem.objects.filter(product = product, cart = cart)
    cart_item.delete()

    return redirect('cart')

def cart(request, total=0, quantity=0, tax= 0, grand_total=0, cart_items={}):
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.all().filter(user=request.user)
    else:
        cart = Cart.objects.all().filter(cart_id = _get_cart_id(request))
        cart_items= CartItem.objects.filter(cart = cart[:1], is_active = True)

    for cart_item in cart_items:
        quantity += cart_item.quantity
        total += cart_item.quantity * cart_item.product.price
    tax = (2 * total)/ 100
    grand_total = total + tax


    context = {
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items': cart_items
    }
    
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, tax= 0, grand_total=0, cart_items=None):
        
        try:
            if request.user.is_authenticated:
                cart = Cart.objects.all().filter(user=request.user)
                cart_items = CartItem.objects.all().filter(cart = cart[:1], is_active = True)
            else:
                cart = Cart.objects.all().filter(cart_id = _get_cart_id(request))
                cart_items = CartItem.objects.filter(cart = cart[:1], is_active = True)

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
            'cart_items': cart_items,
        }
        
        return render(request, 'store/checkout.html', context)
