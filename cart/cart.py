from django.conf import settings
from shop.models import Product
from decimal import Decimal
from django.core import serializers
import json
from django.forms.models import model_to_dict
class Cart:
    def __init__(self,request):
        self.session=request.session
        cart=self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[settings.CART_SESSION_ID]={}
        self.cart=cart

    def add(self,product,quantity=1,override_quantity=False):
        product_id=str(product.id)
        if product_id not in self.cart:
            
            self.cart[product_id]={'quantity':0,'price':str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity']=quantity
        else:
            self.cart[product_id]['quantity'] +=quantity

        self.save()
    def __iter__(self):
        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        for product in products:
            #product=json.dumps(model_to_dict(item['product']))
            #product=json.dumps(model_to_dict(product))

            self.cart[str(product.id)]['product']=(product)
        for item in self.cart.values():
            item['price']=float((item['price']))
            item['total_price']=item['price']*item['quantity']
            yield item
    def save(self):
        self.session.modified=True
    def remove(self,product):
        product_id=str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(item['quantity']*Decimal(item['price']) for item in self.cart.values())
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

        
