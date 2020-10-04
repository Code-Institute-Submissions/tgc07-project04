from django.db import models
from django.contrib.auth.models import User

from teams.models import Team

class Service(models.Model):
    service_name = models.CharField(max_length=50, blank=False)
    price = models.PositiveIntegerField(blank=False)
    service_description = models.TextField(blank=False)

    def __str__(self):
        return self.service_name

class Transaction(models.Model):
    date = models.DateField(blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.RESTRICT)
    transaction_ref = models.CharField(blank=False, max_length=100)
    stripe_webhook_id = models.CharField(blank=False, max_length=100)
    paid_by_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} - {self.team.team_name} - \
            {self.service.service_name}'
