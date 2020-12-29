# -*- coding: utf-8 -*-
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from django.http import Http404
from apps.api.models import Customer, Product
from apps.api.serializers import ProductSerializer, ProductDetailSerializer
from apps.api.services import ProductService
from requests import exceptions


class ProductList(generics.ListCreateAPIView):

    lookup_field = 'customer_id'
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser, DjangoModelPermissions)

    def get_queryset(self):
        customer_id = self.kwargs.get('customer_id')
        if not Customer.objects.filter(id=customer_id).exists():
            raise Http404()

        return Product.objects.filter(
            customer=customer_id
        )

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response(
                {
                    'product_id': [
                        'This field is required.'
                    ]
                },
                status.HTTP_400_BAD_REQUEST
            )

        try:
            product = ProductService.get_product_by_id(product_id)
        except exceptions.HTTPError as e:
            exception_message = str(e)
            status_code = e.response.status_code
            if status_code == status.HTTP_404_NOT_FOUND:
                exception_message = 'The requested Product doesn’t exist.'
                status_code = status.HTTP_400_BAD_REQUEST

            return Response(
                {
                    'detail': exception_message
                },
                status_code
            )
        except Exception as e:
            return Response(
                None,
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if not product:
            return Response(
                None,
                status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        customer_favorite_product_data = {
            'customer': kwargs.get('customer_id'),
            'product_id': product.get('id'),
            'product_title': product.get('title'),
            'product_price': product.get('price'),
            'product_image': product.get('image'),
            'review_score': product.get('reviewScore', None),
        }

        serializer = ProductSerializer(data=customer_favorite_product_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):

    lookup_field = 'id'
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAdminUser, DjangoModelPermissions)

    def get_queryset(self):
        customer_favorite_product_id = self.kwargs.get('id')
        customer_id = self.kwargs.get('customer_id')

        customer_favorite_product = Product.objects.filter(
            customer=customer_id,
            id=customer_favorite_product_id
        )

        if not customer_favorite_product:
            raise Http404()

        return customer_favorite_product
