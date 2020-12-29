# -*- coding: utf-8 -*-
from rest_framework import generics, status, views
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from apps.api.models import Customer
from apps.api.serializers import CustomerSerializer


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUser, DjangoModelPermissions)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsAdminUser, DjangoModelPermissions)
