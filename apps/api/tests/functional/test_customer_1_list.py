# -*- coding: utf-8 -*-

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from api import views
from ..utils import TestUtils
from ...models import Customer
from freezegun import freeze_time


class TestCustomerList(APITestCase):
    def setUp(self):
        self.uri = '/customers/'
        self.view = views.CustomerList.as_view()
        self.factory = APIRequestFactory()
        self.user = TestUtils.create_superuser()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.utils = TestUtils()
        self.utils.clear_database_auto_increments()

    def test_should_return_success_and_empty_results_when_there_are_no_registered_customers(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request)

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
    def test_should_return_success_and_populated_results_when_there_are_registered_customers(self):
        self.utils.create_customer_if_not_exists(
            identifier=1,
            name='Test',
            email='test@email.com'
        )

        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request)

        expected_response_status_code = 200
        expected_response_body = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 1,
                    'name': 'Test',
                    'email': 'test@email.com',
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

    @freeze_time('2019-10-01 23:20:20')
    def test_should_create_customer_when_valid_request_body_is_passed(self):
        request_body = {
            'name': 'Customer',
            'email': 'customer@test.com'
        }

        request = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request)

        expected_response_status_code = 201
        expected_response_body = {
            'id': 1,
            'name': 'Customer',
            'email': 'customer@test.com',
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
        response = self.view(request)

        expected_response_status_code = 400
        expected_response_body = {
            'name': [
                'This field is required.'
            ],
            'email': [
                'This field is required.'
            ]
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_bad_request_when_invalid_email_is_passed(self):
        request_body = {
            'name': 'Customer',
            'email': 'invalid_email'
        }

        request = self.factory.post(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request)

        expected_response_status_code = 400
        expected_response_body = {
            'email': [
                'Enter a valid email address.'
            ]
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_bad_request_when_two_customers_try_to_sign_up_with_same_email(self):
        request_body = {
            'name': 'Customer',
            'email': 'customer@test.com'
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
        response = self.view(request)

        request_two.user = self.user
        response_two = self.view(request_two)

        expected_response_status_code = 400
        expected_response_body = {
            'email': [
                'customer with this email already exists.'
            ]
        }

        self.utils.assert_response(
            response_two,
            expected_response_status_code,
            expected_response_body
        )
