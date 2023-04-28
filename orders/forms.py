from django import forms
from .models import Order
from django.forms import Textarea,TextInput
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=[
        'first_name','last_name','email','phone','Address','postal_code','city','paid'
        ]
        widgets={
            'paid':forms.HiddenInput()
        }
        