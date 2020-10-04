# Generated by Django 3.1.1 on 2020-10-04 06:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_auto_20200925_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]