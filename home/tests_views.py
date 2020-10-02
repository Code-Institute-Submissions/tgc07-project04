from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class HomeViewTestCase(TestCase):
    def test_get_response(self):
        response = self.client.get(reverse('home_route'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

class PricingViewTestCase(TestCase):
    def test_get_response(self):
        response = self.client.get(reverse('pricing_route'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/pricing.html')

class UserProfileViewTestCase(TestCase):
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

    def test_get_response(self):
        response = self.client.get(reverse('user_profile_route'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/user-profile.html')
