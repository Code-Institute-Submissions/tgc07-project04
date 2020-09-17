from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from datetime import date

from .models import *

class CreateTaskViewTestCase(TestCase):
    def setUp(self):
        self.task_creator = User(
            username = "test_task_creator",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.task_creator.save()
        # Log in user
        self.client.force_login(self.task_creator, backend=None)

        self.assignee = User(
            username = "test_assignee",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.assignee.save()

        self.team = Team(team_name="Test Team Name")
        self.team.save()

        self.membership_task_creator = Membership(
                user = self.task_creator,
                team = self.team,
                is_admin = True
        )
        self.membership_task_creator.save()
    
        self.membership_assignee = Membership(
                user = self.assignee,
                team = self.team,
                is_admin = False
        )
        self.membership_assignee.save()

        self.stage = Stage(label="Test Stage")
        self.stage.save()

        self.priority_level = PriorityLevel(priority_level="Urgent")
        self.priority_level.save()

        self.severity_level = SeverityLevel(severity_level="Critical")
        self.severity_level.save()

    def test_get_response(self):
        response = self.client.get(reverse(
            'create_task_route', kwargs={'team_id':self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/create-task.html')

    def test_create_task(self):
        response = self.client.post(reverse(
            'create_task_route', kwargs={'team_id':self.team.id}), {
                "title": "My Test Task",
                "description": "Test description",
                "date_due": date.today(),
                "team": str(self.team.id),
                "stage": str(self.stage.id),
                "priority_level": str(self.priority_level.id),
                "severity_level": str(self.severity_level.id),
                "assignee": [str(self.assignee.id), str(self.task_creator.id)]
        })
        db_title = Task.objects.filter(title="My Test Task")
        self.assertEqual(db_title.count(), 1)
        db_description = Task.objects.filter(description="Test description")
        self.assertEqual(db_title.count(), 1)
        db_date = Task.objects.filter(date_due=date.today())
        self.assertEqual(db_date.count(), 1)
        db_team = Task.objects.filter(team=self.team)
        self.assertEqual(db_team.count(), 1)
        db_stage = Task.objects.filter(stage=self.stage)
        self.assertEqual(db_stage.count(), 1)
        db_priority_level = Task.objects.filter(
            priority_level=self.priority_level)
        self.assertEqual(db_priority_level.count(), 1)
        db_severity_level = Task.objects.filter(
            severity_level=self.severity_level)
        self.assertEqual(db_severity_level.count(), 1)
        db_assignee_1 = Task.objects.filter(assignee=self.assignee)
        self.assertEqual(db_assignee_1.count(), 1)
        db_assignee_2 = Task.objects.filter(assignee=self.task_creator)
        self.assertEqual(db_assignee_2.count(), 1)

class UpdateTaskViewTestCase(TestCase):
    def setUp(self):
        self.task_creator = User(
            username = "test_task_creator",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.task_creator.save()
        # Log in user
        self.client.force_login(self.task_creator, backend=None)

        self.assignee = User(
            username = "test_assignee",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.assignee.save()

        self.team = Team(team_name="Test Team Name")
        self.team.save()

        self.membership_task_creator = Membership(
                user = self.task_creator,
                team = self.team,
                is_admin = True
        )
        self.membership_task_creator.save()
    
        self.membership_assignee = Membership(
                user = self.assignee,
                team = self.team,
                is_admin = False
        )
        self.membership_assignee.save()

        self.stage = Stage(label="Test Stage")
        self.stage.save()

        self.priority_level = PriorityLevel(priority_level="Urgent")
        self.priority_level.save()

        self.severity_level = SeverityLevel(severity_level="Critical")
        self.severity_level.save()

        self.task = Task(
            title = "My Test Task",
            team = self.team,
            task_creator = self.task_creator,
            stage = self.stage,
            priority_level = self.priority_level,
            severity_level = self.severity_level
        )
        self.task.save()

    def test_get_response(self):
        response = self.client.get(reverse(
            'update_task_route', kwargs={
                'team_id': self.team.id,
                'task_id': self.task.id
        }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/update-task.html')

    def test_update_task(self):
        response = self.client.post(reverse(
            'update_task_route', kwargs={
                'team_id': self.team.id,
                'task_id': self.task.id
        }), {
                "title": "My Test Task",
                "description": "Test description",
                "date_due": date.today(),
                "team": str(self.team.id),
                "stage": str(self.stage.id),
                "priority_level": str(self.priority_level.id),
                "severity_level": str(self.severity_level.id),
                "assignee": [str(self.assignee.id), str(self.task_creator.id)]
        })
        db_title = Task.objects.filter(title="My Test Task")
        self.assertEqual(db_title.count(), 1)
        db_description = Task.objects.filter(description="Test description")
        self.assertEqual(db_title.count(), 1)
        db_date = Task.objects.filter(date_due=date.today())
        self.assertEqual(db_date.count(), 1)
        db_team = Task.objects.filter(team=self.team)
        self.assertEqual(db_team.count(), 1)
        db_stage = Task.objects.filter(stage=self.stage)
        self.assertEqual(db_stage.count(), 1)
        db_priority_level = Task.objects.filter(
            priority_level=self.priority_level)
        self.assertEqual(db_priority_level.count(), 1)
        db_severity_level = Task.objects.filter(
            severity_level=self.severity_level)
        self.assertEqual(db_severity_level.count(), 1)
        db_assignee_1 = Task.objects.filter(assignee=self.assignee)
        self.assertEqual(db_assignee_1.count(), 1)
        db_assignee_2 = Task.objects.filter(assignee=self.task_creator)
        self.assertEqual(db_assignee_2.count(), 1)

class DeleteTaskViewTestCase(TestCase):
    def setUp(self):
        self.task_creator = User(
            username = "test_task_creator",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.task_creator.save()
        # Log in user
        self.client.force_login(self.task_creator, backend=None)

        self.assignee = User(
            username = "test_assignee",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.assignee.save()

        self.team = Team(team_name="Test Team Name")
        self.team.save()

        self.membership_task_creator = Membership(
                user = self.task_creator,
                team = self.team,
                is_admin = True
        )
        self.membership_task_creator.save()
    
        self.membership_assignee = Membership(
                user = self.assignee,
                team = self.team,
                is_admin = False
        )
        self.membership_assignee.save()

        self.stage = Stage(label="Test Stage")
        self.stage.save()

        self.priority_level = PriorityLevel(priority_level="Urgent")
        self.priority_level.save()

        self.severity_level = SeverityLevel(severity_level="Critical")
        self.severity_level.save()

        self.task = Task(
            title = "My Test Task",
            team = self.team,
            task_creator = self.task_creator,
            stage = self.stage,
            priority_level = self.priority_level,
            severity_level = self.severity_level
        )
        self.task.save()

    def test_get_response(self):
        response = self.client.get(reverse(
            'delete_task_route', kwargs={
                'team_id': self.team.id,
                'task_id': self.task.id
        }))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/delete-task.html')

    def test_delete_task(self):
        response = self.client.post(reverse(
            'delete_task_route', kwargs={
                'team_id': self.team.id,
                'task_id': self.task.id
        }))
        db_title = Task.objects.filter(title="My Test Task")
        self.assertEqual(db_title.count(), 0)

class ReadTaskViewTestCase(TestCase):
    def setUp(self):
        self.task_creator = User(
            username = "test_task_creator",
            email = "team_member@mailinator.com",
            password = "pass123word"
        )
        self.task_creator.save()
        # Log in user
        self.client.force_login(self.task_creator, backend=None)

        self.team = Team(team_name="Test Team Name")
        self.team.save()

        self.membership_task_creator = Membership(
                user = self.task_creator,
                team = self.team,
                is_admin = True
        )
        self.membership_task_creator.save()

        self.stage = Stage(label="Test Stage")
        self.stage.save()

        self.priority_level = PriorityLevel(priority_level="Urgent")
        self.priority_level.save()

        self.severity_level = SeverityLevel(severity_level="Critical")
        self.severity_level.save()

        self.task = Task(
            title = "My Test Task",
            team = self.team,
            task_creator = self.task_creator,
            stage = self.stage,
            priority_level = self.priority_level,
            severity_level = self.severity_level
        )
        self.task.save()

    def test_get_response(self):
        response = self.client.get(reverse(
            'tasks_team_route', kwargs={'team_id': self.team.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/read-tasks-team.html')

