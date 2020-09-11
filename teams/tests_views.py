from django.test import TestCase
from django.urls import reverse

from .models import Team

class CreateTeamViewTestCase(TestCase):
    def test_get_response(self):
        response = self.client.get(reverse('create_team_route'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/create-team.html')

class UpdateTeamViewTestCase(TestCase):
    def setUp(self):
        self.team = Team(team_name="Test Team Name")
        self.team.save()
    
    def test_get_response(self):
        response = self.client.get(reverse(
            'update_team_route', kwargs={'team_id':self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/update-team.html')
