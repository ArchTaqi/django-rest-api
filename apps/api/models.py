# -*- coding: utf-8 -*-

from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Name: {0}, Email: {1}'.format(self.name, self.email)

    class Meta:

        db_table = 'tbl_customers'
        ordering = ['id']


class Product(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, db_column='customer_id')
    product_id = models.CharField(max_length=200)
    product_title = models.CharField(max_length=200)
    product_price = models.FloatField()
    product_image = models.URLField(max_length=200)
    review_score = models.FloatField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Customer: {0}, ProductID: {1}'.format(self.customer, self.product_id)

    class Meta:
        db_table = 'tbl_customer_products'
        ordering = ['id']
        unique_together = [
            ['customer', 'product_id'],
        ]