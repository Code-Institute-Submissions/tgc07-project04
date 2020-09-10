# Generated by Django 3.1.1 on 2020-09-10 05:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0006_auto_20200910_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignee',
            field=models.ManyToManyField(blank=True, null=True, related_name='task_assignee', to=settings.AUTH_USER_MODEL),
        ),
    ]
