from django.test import TestCase
from django.contrib.auth.models import User

from .forms import *

class TeamFormTestCase(TestCase):
    def setUp(self):
        self.team_member = User(
            username = "test_team_member",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.team_member.save()

    def test_form_valid(self):
        form = TeamForm({
            "team_name": "My Test Team",
            "team_member" : [self.team_member]
        })
        self.assertTrue(form.is_valid())

    def test_team_name_required(self):
        form = TeamForm({
            "team_name": None,
            "team_member" : [self.team_member]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('team_name', form.errors.keys())
        self.assertEqual(
            form.errors['team_name'][0], 'This field is required.')

    def test_team_member_required(self):
        form = TeamForm({
            "team_name": "My Test Team",
            "team_member" : None
        })
        self.assertFalse(form.is_valid())
        self.assertIn('team_member', form.errors.keys())
        self.assertEqual(
            form.errors['team_member'][0], 'This field is required.')

    def test_form_meta_fields(self):
        form = TeamForm()
        self.assertEqual(form.Meta.fields, '__all__')
