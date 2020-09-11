from django.test import TestCase
from django.urls import reverse

class CreateTeamViewTestCase(TestCase):
    def test_get_response(self):
        response = self.client.get(reverse('create_team_route'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teams/create-team.html')
