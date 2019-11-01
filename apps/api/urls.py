# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^auth/$', views.Auth.as_view(), name='auth'),
    url(r'^customers/(?P<id>\d+)$', views.CustomerDetail.as_view(), name='customer-detail'),
    url(r'^customers/$', views.CustomerList.as_view(), name='customer-list'),
    url(r'^customers/(?P<customer_id>\d+)/favorite-products/$', views.ProductList.as_view(), name='customer-favorite-product-list'),
    url(r'^customers/(?P<customer_id>\d+)/favorite-products/(?P<id>\d+)$', views.ProductDetail.as_view(), name='customer-favorite-product-detail'),
]
