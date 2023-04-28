from django.contrib import admin
from .models import Category,Product

@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['category','name','image','slug','price','available']
    list_filter=['category','price','available']
    prepopulated_fields={'slug':('name',)}

