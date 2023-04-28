from django.shortcuts import render,redirect
from django.urls  import reverse
from .forms import OrderCreateForm
from cart.cart import Cart
from .models import OrderItem
from .tasks import order_created
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


def create_order(request):
    cart=Cart(request)
    if request.method=='POST':
        form=OrderCreateForm(request.POST)
        if form.is_valid():
            order=form.save()
            for item in cart:
                #product=json.dumps(item['product'],cls=DjangoJSONEncoder)
                #product = serializers.serialize("json", [item['product']])
                OrderItem.objects.create(order=order,product=(item['product']),price=(item['price']),quantity=item['quantity'])

            cart.clear()
            #order_created(order.id)
        #return render(request,'orders/created.html',{'order':order})
        request.session['order_id']=order.id
        return redirect(reverse('payment:process'))
    else:
        form=OrderCreateForm()
    context={'form':form,'cart':cart}
    return render(request,'orders/create_order.html',context)



