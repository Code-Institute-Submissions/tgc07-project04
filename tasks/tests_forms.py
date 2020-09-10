from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date

from .models import *
from .forms import *

class StageFormTestCase(TestCase):
    def test_form_valid(self):
        form = StageForm({"label": "My Test Stage"})
        self.assertTrue(form.is_valid())

    def test_required_field(self):
        form = StageForm({"label": None})
        self.assertFalse(form.is_valid())
        self.assertIn('label', form.errors.keys())
        self.assertEqual(
            form.errors['label'][0], 'This field is required.')

class PriorityLevelFormTestCase(TestCase):
    def test_form_valid(self):
        form = PriorityLevelForm({"priority_level": "Urgent"})
        self.assertTrue(form.is_valid())

    def test_required_field(self):
        form = PriorityLevelForm({"priority_level": None})
        self.assertFalse(form.is_valid())
        self.assertIn('priority_level', form.errors.keys())
        self.assertEqual(
            form.errors['priority_level'][0], 'This field is required.')

class SeverityLevelFormTestCase(TestCase):
    def test_form_valid(self):
        form = SeverityLevelForm({"severity_level": "My Test Stage"})
        self.assertTrue(form.is_valid())

    def test_required_field(self):
        form = SeverityLevelForm({"severity_level": None})
        self.assertFalse(form.is_valid())
        self.assertIn('severity_level', form.errors.keys())
        self.assertEqual(
            form.errors['severity_level'][0], 'This field is required.')

class TaskFormTestCase(TestCase):
    def setUp(self):
        self.task_creator = User(
            username = "test_task_creator",
            email = "task_creator@mailinator.com",
            password = "pass123word"
        )
        self.task_creator.save()

        self.stage = Stage(label="Test Stage")
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

    def test_form_valid(self):
        form = TaskForm({
            "title": "My Test Team",
            "description" : "Test description",
            "date_due" : date.today(),
            "task_creator" : self.task_creator,
            "stage" : self.stage,
            "priority_level" : self.priority_level,
            "severity_level" : self.severity_level,
            "assignee" : [self.assignee]
        })
        self.assertTrue(form.is_valid())

    def test_title_required(self):
        form = TaskForm({
            "title": None,
            "description" : "Test description",
            "date_due" : date.today(),
            "task_creator" : self.task_creator,
            "stage" : self.stage,
            "priority_level" : self.priority_level,
            "severity_level" : self.severity_level,
            "assignee" : [self.assignee]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(
            form.errors['title'][0], 'This field is required.')

    def test_description_not_required(self):
        form = TaskForm({
            "title": "My Test Team",
            "description" : None,
            "date_due" : date.today(),
            "task_creator" : self.task_creator,
            "stage" : self.stage,
            "priority_level" : self.priority_level,
            "severity_level" : self.severity_level,
            "assignee" : [self.assignee]
        })
        self.assertTrue(form.is_valid())

    def test_date_due_not_required(self):
        form = TaskForm({
            "title": "My Test Team",
            "description" : "Test description",
            "date_due" : None,
            "task_creator" : self.task_creator,
            "stage" : self.stage,
            "priority_level" : self.priority_level,
            "severity_level" : self.severity_level,
            "assignee" : [self.assignee]
        })
        self.assertTrue(form.is_valid())

    def test_task_creator_required(self):
        form = TaskForm({
            "title": "My Test Team",
            "description" : "Test description",
            "date_due" : date.today(),
            "task_creator" : None,
            "stage" : self.stage,
            "priority_level" : self.priority_level,
            "severity_level" : self.severity_level,
            "assignee" : [self.assignee]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('task_creator', form.errors.keys())
        self.assertEqual(
            form.errors['task_creator'][0], 'This field is required.')

    def test_stage_required(self):
        form = TaskForm({
            "title": "My Test Team",
            "description" : "Test description",
            "date_due" : date.today(),
            "task_creator" : self.task_creator,
            "stage" : None,
            "priority_level" : self.priority_level,
            "severity_level" : self.severity_level,
            "assignee" : [self.assignee]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('stage', form.errors.keys())
        self.assertEqual(
            form.errors['stage'][0], 'This field is required.')

    def test_priority_level_required(self):
        form = TaskForm({
            "title": "My Test Team",
            "description" : "Test description",
            "date_due" : date.today(),
            "task_creator" : self.task_creator,
            "stage" : self.stage,
            "priority_level" : None,
            "severity_level" : self.severity_level,
            "assignee" : [self.assignee]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('priority_level', form.errors.keys())
        self.assertEqual(
            form.errors['priority_level'][0], 'This field is required.')

    def test_severity_level_required(self):
        form = TaskForm({
            "title": "My Test Team",
            "description" : "Test description",
            "date_due" : date.today(),
            "task_creator" : self.task_creator,
            "stage" : self.stage,
            "priority_level" : self.priority_level,
            "severity_level" : None,
            "assignee" : [self.assignee]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('severity_level', form.errors.keys())
        self.assertEqual(
            form.errors['severity_level'][0], 'This field is required.')

    def test_assignee_not_required(self):
        form = TaskForm({
            "title": "My Test Team",
            "description" : "Test description",
            "date_due" : date.today(),
            "task_creator" : self.task_creator,
            "stage" : self.stage,
            "priority_level" : self.priority_level,
            "severity_level" : self.severity_level,
            "assignee" : None
        })
        self.assertTrue(form.is_valid())




