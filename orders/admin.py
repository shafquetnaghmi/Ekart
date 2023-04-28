from django.contrib import admin
from .models import Order ,OrderItem

class OrderItemInline(admin.TabularInline):
    model=OrderItem
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['first_name','email','phone','Address','postal_code','city','updated','paid']
    list_filter=['postal_code','paid','created']
    inlines=[OrderItemInline]
