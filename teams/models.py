from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=50, blank=False)
    team_members = models.ManyToManyField(User, through="Membership")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['team_name'], name='unique_team_name')
        ]

    def __str__(self):
        return self.team_name

class Membership(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_membership')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_admin = models.BooleanField(blank=True, default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'team'], name='unique_membership')
        ]

    def __str__(self):
        return f"User:{self.user}, Team:{self.team}, is_admin:{self.is_admin}"
