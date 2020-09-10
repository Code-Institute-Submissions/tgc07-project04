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

        self.admin_user = User(
            username = "test_admin_user",
            email = "admin_user@mailinator.com",
            password = "pass123word"
        )
        self.admin_user.save()
    
        self.project_manager = User(
            username = "test_project_manager",
            email = "project_manager@mailinator.com",
            password = "pass123word"
        )
        self.project_manager.save()
    
    def test_form_valid(self):
        form = TeamForm({
            "team_name": "My Test Team",
            "team_member" : [self.team_member],
            "admin_user" : [self.admin_user],
            "project_manager" : [self.project_manager]
        })
        self.assertTrue(form.is_valid())

    def test_team_name_required(self):
        form = TeamForm({
            "team_name": None,
            "team_member" : [self.team_member],
            "admin_user" : [self.admin_user],
            "project_manager" : [self.project_manager]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('team_name', form.errors.keys())
        self.assertEqual(
            form.errors['team_name'][0], 'This field is required.')

    def test_team_member_required(self):
        form = TeamForm({
            "team_name": "My Test Team",
            "team_member" : [],
            "admin_user" : [self.admin_user],
            "project_manager" : [self.project_manager]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('team_member', form.errors.keys())
        self.assertEqual(
            form.errors['team_member'][0], 'This field is required.')

    def test_admin_user_required(self):
        form = TeamForm({
            "team_name": "My Test Team",
            "team_member" : [self.team_member],
            "admin_user" : [],
            "project_manager" : [self.project_manager]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('admin_user', form.errors.keys())
        self.assertEqual(
            form.errors['admin_user'][0], 'This field is required.')

    def test_project_manager_required(self):
        form = TeamForm({
            "team_name": "My Test Team",
            "team_member" : [self.team_member],
            "admin_user" : [self.admin_user],
            "project_manager" : []
        })
        self.assertFalse(form.is_valid())
        self.assertIn('project_manager', form.errors.keys())
        self.assertEqual(
            form.errors['project_manager'][0], 'This field is required.')
    
    def test_form_meta_fields(self):
        form = TeamForm()
        self.assertEqual(form.Meta.fields, '__all__')
