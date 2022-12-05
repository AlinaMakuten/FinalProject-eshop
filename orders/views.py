from django.shortcuts import render, redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime
import json
from products.models import Product
from django.http import HttpResponse

def payments(request):
    body = json.loads(request.body)
    print(body)
    # order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])
    #
    # payment = Payment(
    #     user=request.user,
    #     payment_id=body['transID'],
    #     payment_method=body['payment_method'],
    #     amount_paid=order.order_total,
    #     status=body['status'],
    # )
    # payment.save()
    #
    # order.payment = payment
    # order.is_ordered = True
    # order.save()
    #
    # cart_items = CartItem.objects.filter(user=request.user)
    #
    # for item in cart_items:
    #     orderproduct = OrderProduct()
    #     orderproduct.order_id = order.id
    #     orderproduct.payment = payment
    #     orderproduct.user_id = request.user.id
    #     orderproduct.product_id = item.product_id
    #     orderproduct.quantity = item.quantity
    #     orderproduct.product_price = item.product.price
    #     orderproduct.ordered = True
    #     orderproduct.save()
    #
    #     cart_item = CartItem.objects.get(id=item.id)
    #     product_variation = cart_item.variations.all()
    #     orderproduct = OrderProduct.objects.get(id=orderproduct.id)
    #     orderproduct.variations.set(product_variation)
    #     orderproduct.save()
    #
    #     product = Product.objects.get(id=item.product_id)  #sumažins kiekį DB
    #     product.stock -= item.quantity
    #     product.save()
    #
    #
    # CartItem.objects.filter(user=request.user).delete()   #užsakius išvalys krepšelį
    #
    #
    #
    return render(request, 'orders/payments.html')

def place_order(request, total=0, quantity=0,):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('knygos')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = round((21 * total) / 100, 2)
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.street = form.cleaned_data['street']
            data.house = form.cleaned_data['house']
            data.appartment = form.cleaned_data['appartment']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.postal_code = form.cleaned_data['postal_code']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # uzsakymo numeris
            yr = int(datetime.date.today().strftime('%Y'))
            mt = int(datetime.date.today().strftime('%m'))
            dt = int(datetime.date.today().strftime('%d'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20221202
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()


            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }

            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


