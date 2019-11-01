# -*- coding: utf-8 -*-

import requests
from django.conf import settings


class ProductRepository():

    def __init__(self):
        self.BASE_URL = settings.PRODUCT_API_BASE_URL
        self.PRODUCT_ENDPOINT = 'product/'

    def get_product_by_id(self, product_id):
        url = self.BASE_URL + self.PRODUCT_ENDPOINT + product_id

        try:
            response = requests.get(url)
        except Exception as e:
            return None

        return response
