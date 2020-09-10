from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Team(models.Model):
    team_name = models.CharField(max_length=50, blank=False)
    team_member = models.ManyToManyField(User, related_name="team_member")
    admin_user = models.ManyToManyField(User, related_name="admin_user")
    project_manager = models.ManyToManyField(User, related_name="project_manager")

    def __str__(self):
        return self.team_name
