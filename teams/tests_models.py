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

    def test_values(self):
        test = Team(team_name = "test_team")
        test.save()
        
        db_test = get_object_or_404(Team, pk=test.id)

        self.assertEqual(db_test.team_members, test.team_members)

class MembershipModelTestCase(TestCase):
    def setUp(self):
        self.team_member = User(
            username = "test_team_member",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.team_member.save()

        self.team = Team(team_name = "test_team_name")
        self.team.save()

    def test_values(self):
        test = Membership(
            user = self.team_member,
            team = self.team
        )
        test.save()
        
        db_test = get_object_or_404(Membership, pk=test.id)

        self.assertEqual(db_test.user, test.user)
        self.assertEqual(db_test.team, test.team)
        self.assertEqual(db_test.is_admin, False)
