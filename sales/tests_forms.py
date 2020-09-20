# from django.test import TestCase
# from django.contrib.auth.models import User
# from datetime import date

# from .models import *
# from .forms import *
# from teams.models import Team

# class ServiceFormTestCase(TestCase):
#     def test_form_valid(self):
#         form = ServiceForm({
#             "service_name": "Test Service",
#             "price": 12345,
#             "service_description": "Test description"
#         })
#         self.assertTrue(form.is_valid())

#     def test_required_field(self):
#         form = ServiceForm({})
#         self.assertFalse(form.is_valid())
#         self.assertIn('service_name', form.errors.keys())
#         self.assertEqual(
#             form.errors['service_name'][0], 'This field is required.')
#         self.assertIn('price', form.errors.keys())
#         self.assertEqual(
#             form.errors['price'][0], 'This field is required.')
#         self.assertIn('service_description', form.errors.keys())
#         self.assertEqual(
#             form.errors['service_description'][0], 'This field is required.')

# class TransactionFormTestCase(TestCase):
#     def setUp(self):
#         self.team_member = User(
#             username = "test_team_member",
#             email = "team_member@mailinator.com",
#             password = "pass123word"
#         )
#         self.team_member.save()

#         self.team = Team(team_name = "Test Team")
#         self.team.save()
#         self.team.team_members.add(self.team_member)
    
#         self.service = Service(
#             service_name = "1 User",
#             price = 12345,
#             service_description = "Teams consisting of only a single user"
#         )
#         self.service.save()

#     def test_form_valid(self):
#         form = TransactionForm({
#             "date": date.today(),
#             "team" : self.team,
#             "service" : self.service
#         })
#         self.assertTrue(form.is_valid())

#     def test_required_field(self):
#         form = TransactionForm({})
#         self.assertFalse(form.is_valid())
#         self.assertIn('date', form.errors.keys())
#         self.assertEqual(
#             form.errors['date'][0], 'This field is required.')
#         self.assertIn('team', form.errors.keys())
#         self.assertEqual(
#             form.errors['team'][0], 'This field is required.')
#         self.assertIn('service', form.errors.keys())
#         self.assertEqual(
#             form.errors['service'][0], 'This field is required.')
