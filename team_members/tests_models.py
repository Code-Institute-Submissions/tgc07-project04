from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import *

class TeamModelTestCase(TestCase):
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
    
    def test_values(self):
        test = Team(team_name = "Test Team")
        test.save()
        test.team_member.add(self.team_member)
        test.admin_user.add(self.admin_user)
        test.project_manager.add(self.project_manager)
        
        db_test = get_object_or_404(Team, pk=test.id)

        self.assertEqual(db_test.team_member, test.team_member)
        self.assertEqual(db_test.admin_user, test.admin_user)
        self.assertEqual(db_test.project_manager, test.project_manager)
