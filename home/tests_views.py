from django.test import TestCase
from django.urls import reverse

class HomeViewTestCase(TestCase):
    def test_get_response(self):
        response = self.client.get(reverse('home_route'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
