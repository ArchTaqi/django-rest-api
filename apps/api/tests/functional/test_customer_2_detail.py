# -*- coding: utf-8 -*-

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from api import views
from ..utils import TestUtils
from freezegun import freeze_time


class TestCustomerDetail(APITestCase):
    def setUp(self):
        self.default_customer_id = '99'
        self.uri = '/customers/' + self.default_customer_id
        self.view = views.CustomerDetail.as_view()
        self.factory = APIRequestFactory()
        self.user = TestUtils.create_superuser()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.utils = TestUtils()
        self.utils.clear_database_auto_increments()
        self.utils.create_customer_if_not_exists(identifier=int(self.default_customer_id))

    def test_should_return_success_when_retrieve_registered_customer(self):
        request = self.factory.get(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_customer_id)

        expected_response_status_code = 200
        expected_response_body = {
            'id': 99,
            'name': 'Customer',
            'email': 'created_customer@email.com',
            'created_at': '2019-10-01T20:20:20-03:00',
            'updated_at': '2019-10-01T20:20:20-03:00'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_not_found_when_send_request_to_unregistered_customer(self):
        request = self.factory.get(
            '/customers/21',
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=21)

        expected_response_status_code = 404
        expected_response_body = {
            'detail': 'Not found.'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_no_content_when_delete_registered_customer(self):
        request = self.factory.delete(
            self.uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_customer_id)

        expected_response_status_code = 204
        expected_response_body = None

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @freeze_time('2019-10-01 23:20:20')
    def test_should_return_success_when_send_patch_request_to_registered_customer_field(self):
        request_body = {
            'name': 'Patch Customer'
        }

        request = self.factory.patch(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_customer_id)

        expected_response_status_code = 200
        expected_response_body = {
            'id': 99,
            'name': 'Patch Customer',
            'email': 'created_customer@email.com',
            'created_at': '2019-10-01T20:20:20-03:00',
            'updated_at': '2019-10-01T20:20:20-03:00'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    @freeze_time('2019-10-01 23:20:20')
    def test_should_return_success_when_send_put_request_to_registered_customer(self):
        request_body = {
            'name': 'Put Customer',
            'email': 'updated_customer@email.com'
        }

        request = self.factory.put(
            self.uri,
            request_body,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.view(request, id=self.default_customer_id)

        expected_response_status_code = 200
        expected_response_body = {
            'id': 99,
            'name': 'Put Customer',
            'email': 'updated_customer@email.com',
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
        response = self.view(request, id=self.default_customer_id)

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
