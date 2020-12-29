# -*- coding: utf-8 -*-
from rest_framework import serializers
from apps.api.models import Customer


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'
