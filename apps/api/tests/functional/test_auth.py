# -*- coding: utf-8 -*-

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from api import views
from ..utils import TestUtils


class TestAuth(APITestCase):
    def setUp(self):
        self.uri = '/auth/'
        self.test_uri = '/customers/'
        self.view = views.Auth.as_view()
        self.test_view = views.CustomerList.as_view()
        self.factory = APIRequestFactory()
        self.user = TestUtils.create_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()
        self.superuser = TestUtils.create_superuser()
        self.superuser_token = Token.objects.create(user=self.superuser)
        self.superuser_token.save()
        self.utils = TestUtils()

    def test_should_return_user_auth_token_when_valid_credentials_is_passed(self):
        request_body = {
            'username': 'superuser',
            'password': 'test'
        }

        request = self.factory.post(
            self.uri,
            request_body
        )

        response = self.view(request)

        expected_response_status_code = 200
        expected_response_body = {
            'token': self.superuser_token.key
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_bad_request_when_empty_credentials_is_passed(self):
        request_body = {}

        request = self.factory.post(
            self.uri,
            request_body
        )

        response = self.view(request)

        expected_response_status_code = 400
        expected_response_body = {
            "username, password": [
                "This fields are required."
            ]
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_bad_request_when_invalid_credentials_is_passed(self):
        request_body = {
            'username': 'test',
            'password': 'test'
        }

        request = self.factory.post(
            self.uri,
            request_body
        )

        response = self.view(request)

        expected_response_status_code = 400
        expected_response_body = {
            "detail": [
                "Invalid Credentials"
            ]
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_unauthorized_when_request_has_no_authentication_credentials(self):
        request = self.factory.get(
            self.test_uri
        )

        response = self.test_view(request)

        expected_response_status_code = 401
        expected_response_body = {
            'detail': 'Authentication credentials were not provided.'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_unauthorized_when_request_has_invalid_authentication_credentials(self):
        request = self.factory.get(
            self.test_uri,
            HTTP_AUTHORIZATION='Token xxx'
        )

        response = self.test_view(request)

        expected_response_status_code = 401
        expected_response_body = {
            'detail': 'Invalid token.'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_forbidden_when_user_has_no_access_to_resource(self):
        request = self.factory.get(
            self.test_uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.token.key)
        )

        request.user = self.user
        response = self.test_view(request)

        expected_response_status_code = 403
        expected_response_body = {
            'detail': 'You do not have permission to perform this action.'
        }

        self.utils.assert_response(
            response,
            expected_response_status_code,
            expected_response_body
        )

    def test_should_return_success_when_user_has_access_to_resource(self):
        request = self.factory.get(
            self.test_uri,
            HTTP_AUTHORIZATION='Token {}'.format(self.superuser_token.key)
        )

        request.user = self.user
        response = self.test_view(request)

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
