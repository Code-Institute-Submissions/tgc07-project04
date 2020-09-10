from django.test import TestCase
from django.contrib.auth.models import User

from .models import *
from .forms import *

class StageFormTestCase(TestCase):
    def test_form_valid(self):
        form = StageForm({"label": "My Test Stage"})
        self.assertTrue(form.is_valid())

    def test_required_field(self):
        form = StageForm({"label": None})
        self.assertFalse(form.is_valid())
        self.assertIn('label', form.errors.keys())
        self.assertEqual(
            form.errors['label'][0], 'This field is required.')

class PriorityLevelFormTestCase(TestCase):
    def test_form_valid(self):
        form = PriorityLevelForm({"priority_level": "Urgent"})
        self.assertTrue(form.is_valid())

    def test_required_field(self):
        form = PriorityLevelForm({"priority_level": None})
        self.assertFalse(form.is_valid())
        self.assertIn('priority_level', form.errors.keys())
        self.assertEqual(
            form.errors['priority_level'][0], 'This field is required.')

class SeverityLevelFormTestCase(TestCase):
    def test_form_valid(self):
        form = SeverityLevelForm({"severity_level": "My Test Stage"})
        self.assertTrue(form.is_valid())

    def test_required_field(self):
        form = SeverityLevelForm({"severity_level": None})
        self.assertFalse(form.is_valid())
        self.assertIn('severity_level', form.errors.keys())
        self.assertEqual(
            form.errors['severity_level'][0], 'This field is required.')

