# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Customer, Product
# Register your models here.


class CustomerAdmin(admin.ModelAdmin):
    pass


class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)