from django.db import models

from teams.models import Team

# Create your models here.
class Service(models.Model):
    service_name = models.CharField(max_length=50, blank=False)
    price = models.IntegerField(blank=False)
    service_description = models.TextField(blank=False)

    def __str__(self):
        return self.service_name

class Transaction(models.Model):
    date = models.DateField(blank=False)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)
    service = models.ForeignKey(Service, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.date} - {self.team.team_name} - {self.service.service_name}'
