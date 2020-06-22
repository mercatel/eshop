from django.test import TestCase
from django import test


# Create your tests here.
class URLTests(test.TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
