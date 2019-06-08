from django.test import TestCase

from .models import User
# Create your tests here.


class CompanyTestCase(TestCase):

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')