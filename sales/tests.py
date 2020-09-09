from django.test import TestCase
from django.shortcuts import get_object_or_404

from .models import *
from team_members.models import Team

# Create your tests here.
class ServiceModelTestCase(TestCase):
    def test_values(self):
        test_s = Service(
            service_name = "1 User",
            price = 12345,
            service_description = "Teams consisting of only a single user"
        )
        test_s.save()

        db_test_s = get_object_or_404(Service, pk=test_s.id)

        self.assertEqual(db_test_s.service_name, test_s.service_name)
        self.assertEqual(db_test_s.price, test_s.price)
        self.assertEqual(
            db_test_s.service_description, test_s.service_description)

