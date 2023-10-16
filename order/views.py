from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .forms import OrderForm
from .models import Order, Payment, OrderProduct

from cart.models import CartItem
from store.models import Store

import datetime
import json


from django.forms.models import model_to_dict

def place_order(request, total = 0, quantity = 0):
    current_user = request.user

    # if no items in the cart
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax
      
    if request.method == 'POST':
        form = OrderForm(request.POST)

        

        if form.is_valid():            
            # save billing informations
            data = Order()
            data.user =current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.total = total
            data.tax = tax
            data.ip = request.META['REMOTE_ADDR']
            data.save()
            # generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(is_ordered=False, order_number=order_number, user=current_user)
            context = {
                'order': order,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
        
            return render(request, 'order/payment.html', context)
    
    else:
        return render(request, 'cart/checkout.html', form)
    

def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(is_ordered=False, order_number=body['orderID'], user=request.user)

    # Save Transactions details inside Payment mode
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['paymentMethod'],
        status = body['status'],
        amount_paid = order.total + order.tax,
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the Cart Items to Order Products model
    try:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            order_product = OrderProduct()
            order_product.order = order
            order_product.payment = payment
            order_product.user = request.user
            order_product.product = item.product
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.is_ordered = True
            order_product.save()
            
            # Reduce quantities of solded products
            try:
                product = Store.objects.get(id = item.product.id)
                product.stock -= item.quantity
                product.save()
            except:
                pass

        # Clear Cart
        cart_items.delete()


        # Send Order payment email to Customer
        email_subject = 'Thank You for your order '
        message = render_to_string('order/order_received_email.html',{
            'user': request.user,
            'order': order
        })
        to_email = request.user.email
        send_email = EmailMessage(email_subject, message, to=[to_email])
        send_email.send()

        # Send order number and transactions id back to sendData method via Javascript
        data = {
            'order_number': order.order_number,
            'payment_id': payment.payment_id
        }

        return JsonResponse(data)

    except:
        pass



    return render(request, 'order/payment.html')

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(is_ordered=True, order_number=order_number)
        ordered_products = OrderProduct.objects.filter(order_id = order.id)
        payment = Payment.objects.get(payment_id = transID)
        
        

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'payment': payment,
            'grand_total': order.total + order.tax
        }
        return render(request, 'order/order_complete.html', context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect(request, 'home')

    # return render(request, 'order/order_complete.html')

        



