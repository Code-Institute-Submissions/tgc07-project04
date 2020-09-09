from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import *

# Create your tests here.
class TeamMemberModelTestCase(TestCase):
    def setUp(self):
        self.team = Team(team_name="TestTeam")
        self.team.save()
    
    def test_default_values(self):
        test_user = User(
            username = "username_test",
            email = "email_test@mailinator.com",
            password = "pass123word",
        )
        test_user.save()

        test_team_member = TeamMember(
            user = test_user,
            team = self.team
            )
        test_team_member.save()
        
        db_test_user = get_object_or_404(TeamMember, pk=test_user.id)

        print(__name__)
        self.assertEqual(db_test_user.is_admin, False)
        self.assertEqual(db_test_user.is_project_manager, False)

