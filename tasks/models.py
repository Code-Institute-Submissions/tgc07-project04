from django.db import models

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

