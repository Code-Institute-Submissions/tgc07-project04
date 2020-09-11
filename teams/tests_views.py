from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import *

class CreateTeamViewTestCase(TestCase):
    def setUp(self):
        # Create user instance
        self.team_member = User(
            username = "test_team_member",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.team_member.save()
        # Log in user
        self.client.force_login(self.team_member, backend=None)

        # Create team instance
        self.team = Team(team_name="Test Team Name")
        self.team.save()

        # Create membership instance
        self.membership_model = Membership(
                user = self.team_member,
                team = self.team,
                is_admin = True
        )
        self.membership_model.save()
    
    def test_get_response(self):
        response = self.client.get(reverse('create_team_route'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/create-team.html')

    def test_create_team(self):
        response = self.client.post(reverse('create_team_route'), {
            "team_name" : self.team,
            "user" : str(self.team_member.id),
            "team" : str(self.team.id),
            "is_admin" : True
        })
        self.assertEqual(response.status_code, 200)
        db_team = Team.objects.filter(team_name="Test Team Name")
        self.assertEqual(db_team.count(), 1)
        db_membership_user = Membership.objects.filter(user=str(
            self.team_member.id))
        self.assertEqual(db_membership_user.count(), 1)
        db_membership_team = Membership.objects.filter(team=str(self.team.id))
        self.assertEqual(db_membership_team.count(), 1)
        db_membership_is_admin = Membership.objects.filter(is_admin=True)
        self.assertEqual(db_membership_is_admin.count(), 1)

class UpdateTeamViewTestCase(TestCase):
    def setUp(self):
        # Create user instance
        self.team_member = User(
            username = "test_team_member",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.team_member.save()
        # Log in user
        self.client.force_login(self.team_member, backend=None)

        # Create team instance
        self.team = Team(team_name="Test Team Name")
        self.team.save()
    
    def test_get_response(self):
        response = self.client.get(reverse(
            'update_team_route', kwargs={'team_id':self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/update-team.html')
