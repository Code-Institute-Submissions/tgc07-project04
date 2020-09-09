from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.team_name

class TeamMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(blank=False, default=False)
    is_project_manager = models.BooleanField(blank=False, default=False)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)

    def __str__(self):
        return self.user.username