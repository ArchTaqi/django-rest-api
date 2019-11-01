# -*- coding: utf-8 -*-

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from api import views
from ..utils import TestUtils
from freezegun import freeze_time


class TestCustomerDetail(APITestCase):
    def setUp(self):
        self.default_customer_id = '77'
        self.default_favorite_product_id = '1'
        self.uri = '/customers/{0}/favorite-products/{1}'.format(self.default_customer_id, self.default_favorite_product_id)
        self.view = views.ProductDetail.as_view()
        self.factory = APIRequestFactory()
        self.user = TestUtils.create_superuser()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.utils = TestUtils()
        self.utils.clear_database_auto_increments()
        self.customer = self.utils.create_customer_if_not_exists(identifier=int(self.default_customer_id))
        self.favorite_product = self.utils.create_favorite_product_if_not_exists(self.customer)

    def test_should_return_success_when_retrieve_registered_favorite_product(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_favorite_product_id, customer_id=self.default_customer_id)

        expected_response_status_code = 200
        expected_response_body = {
            'id': 1,
            'product_id': 'q1w2e3r4',
            'product_title': 'Test',
            'product_price': 1000.0,
            'product_image': 'http://google.com/image',
            'review_score': None,
            'created_at': '2019-10-01T20:20:20-03:00',
            'updated_at': '2019-10-01T20:20:20-03:00'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_not_found_when_send_request_to_unregistered_favorite_product(self):
        request = self.factory.get(
            '/customers/{0}/favorite-products/21'.format(self.default_customer_id),
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=21, customer_id=self.default_customer_id)

        expected_response_status_code = 404
        expected_response_body = {
            'detail': 'Not found.'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_no_content_when_delete_registered_favorite_product(self):
        request = self.factory.delete(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_favorite_product_id, customer_id=self.default_customer_id)

        expected_response_status_code = 204
        expected_response_body = None

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @freeze_time('2019-10-01 23:20:20')
    def test_should_return_success_when_send_patch_request_to_registered_favorite_product_field(self):
        request_body = {
            'product_title': 'Patch Title'
        }

        request = self.factory.patch(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_favorite_product_id, customer_id=self.default_customer_id)

        expected_response_status_code = 200
        expected_response_body = {
            'id': 1,
            'product_id': 'q1w2e3r4',
            'product_title': 'Patch Title',
            'product_price': 1000.0,
            'product_image': 'http://google.com/image',
            'review_score': None,
            'created_at': '2019-10-01T20:20:20-03:00',
            'updated_at': '2019-10-01T20:20:20-03:00'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @freeze_time('2019-10-01 23:20:20')
    def test_should_return_success_when_send_put_request_to_registered_favorite_product(self):
        request_body = {
            'product_id': '4r3e2w1q',
            'product_title': 'Put Title',
            'product_price': 5000.0,
            'product_image': 'http://google.com/put/image'
        }

        request = self.factory.put(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_favorite_product_id, customer_id=self.default_customer_id)

        expected_response_status_code = 200
        expected_response_body = {
            'id': 1,
            'product_id': '4r3e2w1q',
            'product_title': 'Put Title',
            'product_price': 5000.0,
            'product_image': 'http://google.com/put/image',
            'review_score': None,
            'created_at': '2019-10-01T20:20:20-03:00',
            'updated_at': '2019-10-01T20:20:20-03:00'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_bad_request_when_send_put_request_with_empty_body(self):
        request_body = {}

        request = self.factory.put(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_favorite_product_id, customer_id=self.default_customer_id)

        expected_response_status_code = 400
        expected_response_body = {
            'product_id': [
                'This field is required.'
            ],
            'product_title': [
                'This field is required.'
            ],
            'product_price': [
                'This field is required.'
            ],
            'product_image': [
                'This field is required.'
            ]
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )
