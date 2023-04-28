from django.shortcuts import render,get_object_or_404,redirect
from shop.models import Product
from django.views.decorators.http import require_POST
from .forms import CartAddProductForm
from .cart import Cart
import json
from django.core.serializers.json import DjangoJSONEncoder
@require_POST
def cart_add(request,product_id):
    cart=Cart(request)
    product=get_object_or_404(Product,id=product_id)
    form=CartAddProductForm(request.POST)
    if form.is_valid():
        cd=form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    cart=Cart(request)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart=Cart(request)
    #context={'cart':json.dumps(cart,cls=DjangoJSONEncoder)}
    context={'cart':cart}
    return render(request,'cart/cart_detail.html',context)




