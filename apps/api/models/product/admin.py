# -*- coding: utf-8 -*-
from django.contrib import admin
from .model import Product

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
