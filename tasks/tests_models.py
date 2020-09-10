from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from datetime import date

from .models import *
from team_members.models import *

# Create your tests here.
class StageModelTestCase(TestCase):
    def test_values(self):
        test_stage = Stage(label="Completed Stage")
        test_stage.save()

        db_test_stage = get_object_or_404(Stage, pk=test_stage.id)

        self.assertEqual(db_test_stage.label, test_stage.label)

class PriorityLevelModelTestCase(TestCase):
    def test_values(self):
        test_p = PriorityLevel(priority_level="Urgent")
        test_p.save()

        db_test_p = get_object_or_404(PriorityLevel, pk=test_p.id)

        self.assertEqual(db_test_p.priority_level, test_p.priority_level)

class SeverityLevelModelTestCase(TestCase):
    def test_values(self):
        test_s = SeverityLevel(severity_level="Critical")
        test_s.save()

        db_test_s = get_object_or_404(SeverityLevel, pk=test_s.id)

        self.assertEqual(db_test_s.severity_level, test_s.severity_level)

class TaskModelTestCase(TestCase):
    def setUp(self):
        self.task_creator = User(
            username = "test_task_creator",
            email = "task_creator@mailinator.com",
            password = "pass123word"
        )
        self.task_creator.save()

        self.stage = Stage(label="Completed Stage")
        self.stage.save()

        self.priority_level = PriorityLevel(priority_level="Urgent")
        self.priority_level.save()

        self.severity_level = SeverityLevel(severity_level="Critical")
        self.severity_level.save()

        self.assignee = User(
            username = "test_assignee",
            email = "assignee@mailinator.com",
            password = "pass123word"
        )
        self.assignee.save()
    
    def test_values(self):
        test_t = Task(
            title = "Solve testing bug",
            description = "Test description, test description, test \
                description",
            date_due = date.today(),
            task_creator = self.task_creator,
            stage = self.stage,
            priority_level = self.priority_level,
            severity_level = self.severity_level
        )
        test_t.save()
        test_t.assignee.add(self.assignee)

        db_test_t = get_object_or_404(Task, pk=test_t.id)

        self.assertEqual(db_test_t.title, test_t.title)
        self.assertEqual(db_test_t.description, test_t.description)
        self.assertEqual(db_test_t.date_due, test_t.date_due)
        self.assertEqual(db_test_t.task_creator, test_t.task_creator)
        self.assertEqual(db_test_t.stage, test_t.stage)
        self.assertEqual(db_test_t.priority_level, test_t.priority_level)
        self.assertEqual(db_test_t.severity_level, test_t.severity_level)
        self.assertEqual(db_test_t.assignee.count(), 1)

class ChecklistItemModelTestCase(TestCase):
    def setUp(self):
        self.task_creator = User(
            username = "test_task_creator",
            email = "task_creator@mailinator.com",
            password = "pass123word"
        )
        self.task_creator.save()

        self.stage = Stage(label="Completed Stage")
        self.stage.save()

        self.priority_level = PriorityLevel(priority_level="Urgent")
        self.priority_level.save()

        self.severity_level = SeverityLevel(severity_level="Critical")
        self.severity_level.save()

        self.assignee = User(
            username = "test_assignee",
            email = "assignee@mailinator.com",
            password = "pass123word"
        )
        self.assignee.save()

        self.task = Task(
            title = "Solve testing bug",
            description = "Test description, test description, test \
                description",
            date_due = date.today(),
            task_creator = self.task_creator,
            stage = self.stage,
            priority_level = self.priority_level,
            severity_level = self.severity_level
        )
        self.task.save()
        self.task.assignee.add(self.assignee)
    
    def test_values(self):
        test_c = ChecklistItem(
            item = "Test checklist item",
            task = self.task
        )
        test_c.save()

        db_test_c = get_object_or_404(ChecklistItem, pk=test_c.id)

        self.assertEqual(db_test_c.item, test_c.item)
        self.assertEqual(db_test_c.completed, False)
        self.assertEqual(db_test_c.task, test_c.task)

