"""
Tests for the hello app.
"""
from django.test import TestCase, Client
from django.urls import reverse

class HelloViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        """Test the index view loads correctly."""
        response = self.client.get(reverse('hello:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'hello/index.html')

    def test_api_view(self):
        """Test the API endpoint returns correct JSON."""
        response = self.client.get(reverse('hello:hello_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Hello World from Django API!')
        self.assertEqual(response.json()['status'], 'success')