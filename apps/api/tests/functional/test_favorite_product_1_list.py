# -*- coding: utf-8 -*-

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from unittest.mock import MagicMock, PropertyMock, patch
from api import views, services
from ..utils import TestUtils
from ...models import Customer
from freezegun import freeze_time
from requests import exceptions


class TestProductList(APITestCase):
    def setUp(self):
        self.default_customer_id = '88'
        self.uri = '/customers/{0}/favorite-products/'.format(self.default_customer_id)
        self.view = views.ProductList.as_view()
        self.factory = APIRequestFactory()
        self.user = TestUtils.create_superuser()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.utils = TestUtils()
        self.utils.clear_database_auto_increments()
        self.customer = self.utils.create_customer_if_not_exists(identifier=int(self.default_customer_id))

    def test_should_return_not_found_when_send_request_to_unregistered_customer_in_favorite_products_path(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=50)

        expected_response_status_code = 404
        expected_response_body = {
            'detail': 'Not found.'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_success_and_empty_results_when_there_are_no_registered_favorite_products(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=self.default_customer_id)

        expected_response_status_code = 200
        expected_response_body = {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @freeze_time('2019-10-01 23:20:20')
    def test_should_return_success_and_populated_results_when_there_are_registered_favorite_products(self):
        self.utils.create_favorite_product_if_not_exists(
            self.customer,
        )

        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=self.default_customer_id)

        expected_response_status_code = 200
        expected_response_body = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'product_id': 'q1w2e3r4',
                    'product_title': 'Test',
                    'product_price': 1000.0,
                    'product_image': 'http://google.com/image',
                    'review_score': None,
                    'created_at': '2019-10-01T20:20:20-03:00',
                    'updated_at': '2019-10-01T20:20:20-03:00'
                }
            ]
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @patch('api.services.ProductService.get_product_by_id')
    @freeze_time('2019-10-01 23:20:20')
    def test_should_create_favorite_products_when_valid_request_body_is_passed(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = {
            'price': 1699,
            'image': 'http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg',
            'brand': 'bébé confort',
            'id': '1bf0f365-fbdd-4e21-9786-da459d78dd1f',
            'title': 'Cadeira para Auto Iseos Bébé Confort Earth Brown'
        }

        request_body = {
            'product_id': '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        }

        request = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=self.default_customer_id)

        expected_response_status_code = 201
        expected_response_body = {
            'id': 1,
            'product_id': '1bf0f365-fbdd-4e21-9786-da459d78dd1f',
            'product_title': 'Cadeira para Auto Iseos Bébé Confort Earth Brown',
            'product_price': 1699,
            'product_image': 'http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg',
            'review_score': None,
            'created_at': '2019-10-01T20:20:20-03:00',
            'updated_at': '2019-10-01T20:20:20-03:00'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_bad_request_when_empty_response_body_is_passed(self):
        request_body = {}

        request = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=self.default_customer_id)

        expected_response_status_code = 400
        expected_response_body = {
            'product_id': [
                'This field is required.'
            ]
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @patch('api.services.ProductService.get_product_by_id')
    def test_should_return_bad_request_when_nonexistent_product_id_is_passed(self, mock_get_product_by_id):
        response_mock = MagicMock()
        type(response_mock).status_code = PropertyMock(return_value=404)

        mock_get_product_by_id.side_effect = exceptions.HTTPError(
            '404 Client Error: Not Found for url: http://api.products.com/api/product/okok',
            response=response_mock
        )

        request_body = {
            'product_id': 'okok'
        }

        request = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=self.default_customer_id)

        expected_response_status_code = 400
        expected_response_body = {
            'detail': 'The requested Product doesn’t exist.'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @patch('api.services.ProductService.get_product_by_id')
    def test_should_return_internal_server_error_when_unexpected_error_occurs(self, mock_get_product_by_id):
        mock_get_product_by_id.side_effect = Exception('Unexpected error')

        request_body = {
            'product_id': 'a\kjlwjfg'
        }

        request = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=self.default_customer_id)

        expected_response_status_code = 500
        expected_response_body = None

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @patch('api.services.ProductService.get_product_by_id')
    def test_should_return_internal_server_error_when_product_api_is_out(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = None

        request_body = {
            'product_id': 'okok'
        }

        request = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=self.default_customer_id)

        expected_response_status_code = 500
        expected_response_body = None

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @patch('api.services.ProductService.get_product_by_id')
    def test_should_return_bad_request_when_the_same_customer_try_register_products_with_same_id(self, mock_get_product_by_id):
        mock_get_product_by_id.return_value = {
            'price': 1699,
            'image': 'http://challenge-api.luizalabs.com/images/1bf0f365-fbdd-4e21-9786-da459d78dd1f.jpg',
            'brand': 'bébé confort',
            'id': '1bf0f365-fbdd-4e21-9786-da459d78dd1f',
            'title': 'Cadeira para Auto Iseos Bébé Confort Earth Brown'
        }

        request_body = {
            'product_id': '1bf0f365-fbdd-4e21-9786-da459d78dd1f'
        }

        request = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request_two = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, customer_id=self.default_customer_id)

        request_two.user = self.user
        response_two = self.view(request_two, customer_id=self.default_customer_id)

        expected_response_status_code = 400
        expected_response_body = {
            'non_field_errors': [
                'The fields customer, product_id must make a unique set.'
            ]
        }

        self.utils.assert_response(
            response_two,
            expected_response_status_code,
            expected_response_body
        )
