from django.db import models
from phone_field import PhoneField
from django.core.validators import MinLengthValidator
from shop.models import Product

class Order(models.Model):
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField()
    phone = PhoneField(blank=False, help_text='Contact phone number')
    Address=models.CharField(max_length=300)
    #Address=models.Textarea()
    postal_code=models.CharField(max_length=10, validators=[MinLengthValidator(4)])
    city=models.CharField(max_length=30)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    paid=models.BooleanField(default=False)

    class Meta:
        indexes=[
            models.Index(fields=['-created'])
        ]
        ordering=['-created']

    def __str__(self):
        return str(self.id)
    def get_total_cost(self):
        return sum((item.quantity*item.price)for item in self.items.all())

class OrderItem(models.Model):
    order=models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='order_items' ,on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveBigIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price *self.quantity
    

      