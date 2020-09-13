from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
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
    
        # Create membership instance
        self.membership_model = Membership(
                user = self.team_member,
                team = self.team,
                is_admin = True
        )
        self.membership_model.save()
    
    def test_get_response(self):
        response = self.client.get(reverse(
            'update_team_route', kwargs={'team_id':self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/update-team.html')

    def test_update_team(self):
        new_data = {"team_name" : "Updated Team Name"}
        response = self.client.post(reverse(
            'update_team_route', kwargs={'team_id':self.team.id}), new_data)
        self.assertEqual(response.status_code, 302)

        # Check database entry has been updated correctly
        db_updated = get_object_or_404(Team, pk=self.team.id)
        for key, value in new_data.items():
            self.assertEquals(getattr(db_updated, key), value)

class DeleteTeamViewTestCase(TestCase):
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
        response = self.client.get(reverse(
            'delete_team_route', kwargs={'team_id':self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/delete-team.html')

    def test_delete_team(self):
        response = self.client.post(reverse(
            'delete_team_route', kwargs={'team_id':self.team.id}))
        self.assertEqual(response.status_code, 302)

        # Check database entry does not exist
        deleted_item = Team.objects.filter(pk=self.team.id).first()
        self.assertEquals(deleted_item, None)

class CreateMembershipViewTestCase(TestCase):
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
        response = self.client.get(reverse('create_membership_route',
            kwargs={'team_id':self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/create-membership.html')

    def test_create_membership(self):
        new_team_member = User(
            username = "new_team_member",
            email = "new_team_member@mailinator.com",
            password = "pass123word"
        )
        new_team_member.save()
        
        response = self.client.post(reverse('create_membership_route',
            kwargs={'team_id':self.team.id}), {
                "user" : str(new_team_member.id),
                "team" : str(self.team.id),
                "is_admin" : True
        })
        # Check redirect
        self.assertEqual(response.status_code, 302)
        # Check that there are 2 memberships in team queried
        db_membership_team = Membership.objects.filter(team=self.team.id)
        self.assertEqual(db_membership_team.count(), 2)
        # Check that there is only 1 membership matching queried user
        db_membership_user_1 = Membership.objects.filter(user=str(
            self.team_member.id))
        self.assertEqual(db_membership_user_1.count(), 1)
        # Check that there is only 1 membership matching queried user
        db_membership_user_2 = Membership.objects.filter(user=str(
            new_team_member.id))
        self.assertEqual(db_membership_user_2.count(), 1)
        # Check that there are 2 memberships matching is_admin query
        db_membership_is_admin = Membership.objects.filter(is_admin=True)
        self.assertEqual(db_membership_is_admin.count(), 2)

class UpdateMembershipViewTestCase(TestCase):
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

        self.new_team_member = User(
            username = "new_team_member",
            email = "new_team_member@mailinator.com",
            password = "pass123word"
        )
        self.new_team_member.save()

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
        response = self.client.get(reverse('update_membership_route', kwargs={
            'team_id': self.team.id,
            'membership_id': self.membership_model.id
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/update-membership.html')

    def test_update_membership(self):
        response = self.client.post(reverse('update_membership_route',
            kwargs={
                'team_id': self.team.id,
                'membership_id': self.membership_model.id
            }), {
                'user': str(self.new_team_member.id),
                'team': str(self.team.id),
                'is_admin': True
        })
        # Check redirect
        self.assertEqual(response.status_code, 302)
        # Check that there is only 1 membership in team queried
        db_membership_team = Membership.objects.filter(team=self.team.id)
        self.assertEqual(db_membership_team.count(), 1)
        # Check that there is no memberships matching queried user
        db_membership_user_1 = Membership.objects.filter(user=str(
            self.team_member.id))
        self.assertEqual(db_membership_user_1.count(), 0)
        # Check that there is only 1 membership matching queried user
        db_membership_user_2 = Membership.objects.filter(user=str(
            self.new_team_member.id))
        self.assertEqual(db_membership_user_2.count(), 1)
        # Check matching is_admin query
        db_membership_is_admin = Membership.objects.filter(is_admin=True)
        self.assertEqual(db_membership_is_admin.count(), 1)
    
class DeleteMembershipViewTestCase(TestCase):
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

        self.new_team_member = User(
            username = "new_team_member",
            email = "new_team_member@mailinator.com",
            password = "pass123word"
        )
        self.new_team_member.save()

        # Create team instance
        self.team = Team(team_name="Test Team Name")
        self.team.save()

        # Create membership instance
        self.membership_model_1 = Membership(
                user = self.team_member,
                team = self.team,
                is_admin = True
        )
        self.membership_model_1.save()
    
        self.membership_model_2 = Membership(
                user = self.new_team_member,
                team = self.team,
                is_admin = False
        )
        self.membership_model_2.save()
    
    def test_get_response(self):
        response = self.client.get(reverse('delete_membership_route', kwargs={
            'team_id': self.team.id,
            'membership_id': self.membership_model_1.id
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/delete-membership.html')

    def test_delete_membership_admin(self):
        response = self.client.post(reverse('delete_membership_route',
            kwargs={
                'team_id': self.team.id,
                'membership_id': self.membership_model_1.id
            }))
        # Check redirect
        self.assertEqual(response.status_code, 302)
        # Check that there are 2 memberships in team queried
        db_membership_team = Membership.objects.filter(team=self.team.id)
        self.assertEqual(db_membership_team.count(), 2)
        # Check that there still membership matching queried user
        db_membership_user_1 = Membership.objects.filter(user=str(
            self.team_member.id))
        self.assertEqual(db_membership_user_1.count(), 1)
        # Check that there is still membership matching queried user
        db_membership_user_2 = Membership.objects.filter(user=str(
            self.new_team_member.id))
        self.assertEqual(db_membership_user_2.count(), 1)
        # Check matching is_admin query
        db_membership_is_admin = Membership.objects.filter(is_admin=True)
        self.assertEqual(db_membership_is_admin.count(), 1)
    
    def test_delete_membership_non_admin(self):
        response = self.client.post(reverse('delete_membership_route',
            kwargs={
                'team_id': self.team.id,
                'membership_id': self.membership_model_2.id
            }))
        # Check redirect
        self.assertEqual(response.status_code, 302)
        # Check that there is only 1 membership in team queried
        db_membership_team = Membership.objects.filter(team=self.team.id)
        self.assertEqual(db_membership_team.count(), 1)
        # Check that there still membership matching queried user
        db_membership_user_1 = Membership.objects.filter(user=str(
            self.team_member.id))
        self.assertEqual(db_membership_user_1.count(), 1)
        # Check that there no membership matching queried user
        db_membership_user_2 = Membership.objects.filter(user=str(
            self.new_team_member.id))
        self.assertEqual(db_membership_user_2.count(), 0)
        # Check matching is_admin query
        db_membership_is_admin = Membership.objects.filter(is_admin=True)
        self.assertEqual(db_membership_is_admin.count(), 1)
    
