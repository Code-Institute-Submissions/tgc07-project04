from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from datetime import date

from .models import *
from teams.models import Team

# Create your tests here.
class ServiceModelTestCase(TestCase):
    def test_values(self):
        test_s = Service(
            service_name = "30 day subscription",
            price = 1000,
            service_description = "Price per team per 30 days. Add as many \
                team members as you like!"
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
            service_name = "1 year subscription",
            price = 10000,
            service_description = "Price per team per year. Pay annually and \
                save over 20%! Unlimited number of team members."
        )
        self.service.save()
    
        self.payer = User(
            username = "test_task_creator",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.payer.save()
        # Log in user
        self.client.force_login(self.payer, backend=None)

    def test_values(self):
        test_t = Transaction(
            date = date.today(),
            team = self.team,
            service = self.service,
            transaction_ref = "qhfo837hdnq23hdqi3hdq3hdq",
            stripe_webhook_id = "hdqi73hdhwdhqw3hdfqkiw3",
            paid_by_user = self.payer
        )
        test_t.save()

        db_test_t = get_object_or_404(Transaction, pk=test_t.id)

        self.assertEqual(db_test_t.date, test_t.date)
        self.assertEqual(db_test_t.team, test_t.team)
        self.assertEqual(db_test_t.service, test_t.service)
        self.assertEqual(db_test_t.transaction_ref, test_t.transaction_ref)
        self.assertEqual(db_test_t.stripe_webhook_id, test_t.stripe_webhook_id)
        self.assertEqual(db_test_t.paid_by_user, test_t.paid_by_user)
