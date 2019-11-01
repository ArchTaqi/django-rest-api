# -*- coding: utf-8 -*-

from ...services import ProductService
from unittest.mock import MagicMock, PropertyMock, patch
import unittest
from requests import Response, exceptions


class TestService(unittest.TestCase):

    @patch('api.repositories.ProductRepository.get_product_by_id')
    def test_get_product_by_id_should_return_none_when_repository_returns_empty_response(self, mock_repository_response):
        mock_repository_response.return_value = None

        self.assertEqual(
            ProductService.get_product_by_id(1),
            None
        )

    @patch('api.repositories.ProductRepository.get_product_by_id')
    def test_get_product_by_id_should_return_exception_when_repository_returns_unsuccessful_request(self, mock_repository_response):
        response_mock = MagicMock()
        response_mock.raise_for_status.side_effect = exceptions.HTTPError(
            '404 Client Error: Not Found for url: http://api.products.com/api/product/okok',
            response=response_mock
        )

        mock_repository_response.return_value = response_mock

        self.assertRaises(
            exceptions.HTTPError,
            ProductService.get_product_by_id,
            1
        )

    @patch('api.repositories.ProductRepository.get_product_by_id')
    def test_get_product_by_id_should_return_response_json_when_repository_returns_valid_response(self, mock_repository_response):
        response_mock = MagicMock()
        response_mock.json.return_value = {'unit': 'test'}

        mock_repository_response.return_value = response_mock

        self.assertEqual(
            ProductService.get_product_by_id(1),
            {'unit': 'test'}
        )
