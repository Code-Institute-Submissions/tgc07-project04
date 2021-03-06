from django.db import models
from django.contrib.auth.models import User

from teams.models import *

# Create your models here.
class Stage(models.Model):
    label = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.label

class PriorityLevel(models.Model):
    priority_level = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.priority_level

class SeverityLevel(models.Model):
    severity_level = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.severity_level

class Task(models.Model):
    title = models.CharField(max_length=50, blank=False)
    description = models.TextField(blank=True, null=True)
    date_due = models.DateField(blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    task_creator = models.ForeignKey(
        User, related_name="task_creator", on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.RESTRICT)
    priority_level = models.ForeignKey(
        PriorityLevel, on_delete=models.RESTRICT)
    severity_level = models.ForeignKey(
        SeverityLevel, on_delete=models.RESTRICT)
    assignee = models.ManyToManyField(
        User, related_name="task_assignee", blank=True)

    def __str__(self):
        return self.title

class ChecklistItem(models.Model):
    item = models.CharField(max_length=50, blank=False)
    completed = models.BooleanField(blank=True, default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.item

