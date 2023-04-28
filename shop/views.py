from django.shortcuts import render
from .models import Product,Category
from django.shortcuts import get_object_or_404
from cart.forms import CartAddProductForm

def ProductList(request,category_slug=None):
    categories=Category.objects.all()
    category=None
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=category)
    else:
        products=Product.objects.all()
    context={"products":products,'categories':categories,'category':category}
    return render(request,'shop/ProductList.html',context)

def ProductDetail(request,id,slug):
    product=get_object_or_404(Product,pk=id,slug=slug)
    cart_add_product_form=CartAddProductForm()
    context={'product':product,'cart_add_product_form':cart_add_product_form }
    return render(request,'shop/ProductDetail.html',context)