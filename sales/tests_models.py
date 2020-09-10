from django.test import TestCase
from django.shortcuts import get_object_or_404

from datetime import date

from .models import *
from teams.models import Team

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

class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.team = Team(team_name="TestTeam")
        self.team.save()

        self.service = Service(
            service_name = "1 User",
            price = 12345,
            service_description = "Teams consisting of only a single user"
        )
        self.service.save()
    
    def test_values(self):
        test_t = Transaction(
            date = date.today(),
            team = self.team,
            service = self.service
        )
        test_t.save()

        db_test_t = get_object_or_404(Transaction, pk=test_t.id)

        self.assertEqual(db_test_t.date, test_t.date)
        self.assertEqual(db_test_t.team, test_t.team)
        self.assertEqual(db_test_t.service, test_t.service)
