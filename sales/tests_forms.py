from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from .models import *
from .forms import *

class ServiceFormTestCase(TestCase):
    def test_form_valid(self):
        form = ServiceForm({
            "service_name": "Test Service",
            "price": 12345,
            "service_description": "Test description"
        })
        self.assertTrue(form.is_valid())

    def test_required_field(self):
        form = ServiceForm({})
        self.assertFalse(form.is_valid())
        self.assertIn('service_name', form.errors.keys())
        self.assertEqual(
            form.errors['service_name'][0], 'This field is required.')
        self.assertIn('price', form.errors.keys())
        self.assertEqual(
            form.errors['price'][0], 'This field is required.')
        self.assertIn('service_description', form.errors.keys())
        self.assertEqual(
            form.errors['service_description'][0], 'This field is required.')


