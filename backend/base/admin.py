from django.contrib import admin
from django.db.models import fields
from .models import *

# Register your models here.

class ProductCreation(admin.ModelAdmin):
    fieldsets = [
        ("Product information", {"fields": ["user", "category", 
        "name", "brand", "image", "description", "price", 
        "is_promoted", "count_in_stock", "numReviews", "rating"]})
    ]

admin.site.register(Product,ProductCreation)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Review)
