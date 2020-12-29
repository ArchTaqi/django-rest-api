# -*- coding: utf-8 -*-

from django.db import models


class Customer(models.Model):
    name = models.CharField(
        max_length=200,
        db_column='name'
    )
    email = models.EmailField(
        max_length=200,
        unique=True,
        db_column='email'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_column='created_at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_column='updated_at'
    )

    def __str__(self):
        return 'Name: {0}, Email: {1}'.format(self.name, self.email)

    class Meta:
        db_table = 'tbl_customers'
        ordering = ['id']
