# Generated by Django 3.1.1 on 2020-09-11 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20200910_0841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='team_member',
            new_name='team_members',
        ),
    ]
