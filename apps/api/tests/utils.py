# -*- coding: utf-8 -*-

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.core import management
from ..models import Customer, Product
from freezegun import freeze_time


class TestUtils(APITestCase):

    def assert_response(self, received_response, expected_status_code, expected_body):
        self.assertEqual(
            received_response.status_code,
            expected_status_code,
            'Expected response status code "{0}", received "{1}" instead.'.format(
                expected_status_code,
                received_response.status_code
            )
        )

        self.assertEqual(
            received_response.data,
            expected_body,
            'Expected response body "{0}", received "{1}" instead.'.format(
                expected_body,
                received_response.data
            )
        )

    @staticmethod
    @freeze_time('2019-10-01 23:20:20')
    def create_customer_if_not_exists(identifier=1, name='Customer', email='created_customer@email.com'):
        if Customer.objects.filter(email=email).exists():
            return Customer.objects.filter(email=email)

        return Customer.objects.create(id=identifier, name=name, email=email)

    @staticmethod
    @freeze_time('2019-10-01 23:20:20')
    def create_favorite_product_if_not_exists(customer, identifier=1, product_id='q1w2e3r4', product_title='Test', product_price=1000.00, product_image='http://google.com/image'):
        if Product.objects.filter(product_id=product_id).exists():
            return Product.objects.filter(product_id=product_id)

        return Product.objects.create(
            id=identifier,
            customer=customer,
            product_id=product_id,
            product_title=product_title,
            product_price=product_price,
            product_image=product_image
        )

    @staticmethod
    def clear_database_auto_increments():
        management.call_command('sqlsequencereset', 'api')

    @staticmethod
    def create_user(username='user', email='testuser@test.com', password='test'):
        User = get_user_model()
        return User.objects.create_user(
            username,
            email=email,
            password=password
        )

    @staticmethod
    def create_superuser(username='superuser', email='superuser@test.com', password='test'):
        User = get_user_model()
        return User.objects.create_superuser(
            username,
            email=email,
            password=password
        )
