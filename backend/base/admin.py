from django.contrib import admin
from django.db.models import fields
from .models import *

# Register your models here.

class ProductCreation(admin.ModelAdmin):
    fieldsets = [
        ("Product information", {"fields": ["user", "subcategory", 
        "name", "brand", "image", "description", "price", 
        "is_promoted", "count_in_stock"]}),
        ("Product parameters", {"fields": ["parameters_id"]})
    ]

admin.site.register(MenuLanguage)
admin.site.register(GeneralInfo)
admin.site.register(RamAmount)
admin.site.register(InternalMemory)
admin.site.register(MemoryInfo)
admin.site.register(OperationalSystem)
admin.site.register(Cpu)
admin.site.register(Gpu)
admin.site.register(ProccessorAndOs)
admin.site.register(Parameters)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Product,ProductCreation)
