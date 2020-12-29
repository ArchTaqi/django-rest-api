# -*- coding: utf-8 -*-

from .repositories import ProductRepository


class ProductService():

    @staticmethod
    def get_product_by_id(product_id):
        product_repository = ProductRepository()

        response = product_repository.get_product_by_id(str(product_id))
        if response is None:
            return None

        response.raise_for_status()

        return response.json()
