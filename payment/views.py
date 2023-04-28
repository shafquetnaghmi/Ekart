from django.shortcuts import render,get_object_or_404,reverse,redirect
from decimal import Decimal
import stripe
from django.conf import settings
from orders.models import Order
from orders.forms import OrderCreateForm
from cart.cart import Cart
from orders.tasks import order_created
stripe.api_key=settings.STRIPE_SECRET_KEY

def payment_process(request):
    order_id=request.session['order_id']
    order=get_object_or_404(Order,id=order_id)
    if request.method=='POST':
        cancel_url=request.build_absolute_uri(reverse('payment:canceled'))
        success_url=request.build_absolute_uri(reverse('payment:completed'))
        session_data={
            'success_url':success_url,
            'cancel_url':cancel_url,
            'mode':'payment',
            'client_reference_id':order.id,
            'line_items':[]
            }
        
        for item in order.items.all():
            session_data['line_items'].append({
            'price_data':{
                'unit_amount':int(item.price)*Decimal('100'),
                'currency':'INR',
            'product_data':{
                'name':item.product.name}
            },
            'quantity':item.quantity
            }),
        session=stripe.checkout.Session.create(**session_data)
        return redirect(session.url,code=303)
    else:
        return render(request,'payment/process.html',locals())
def payment_completed(request):
    order_id=request.session['order_id']
    order=Order.objects.get(id=order_id)
    order.paid=True
    order.save()
    cart=Cart(request)
    #cart.clear()
    order_created(order.id)
    return render(request,'payment/completed.html',{'order_id':order_id,'order':order})
def payment_canceled(request):
    return render(request,'payment/canceled.html')

def OrderConfirmed(request):
    order_id=request.session['order_id']
    order=Order.objects.get(id=order_id)
    order_created(order.id)
    return render(request,'payment/confirm.html',{'order_id':order_id,'order':order})




