from django.test import TestCase
from django.shortcuts import get_object_or_404

from .models import *

# Create your tests here.
class StageModelTestCase(TestCase):
    def test_values(self):
        test_stage = Stage(label="Completed Stage")
        test_stage.save()

        db_test_stage = get_object_or_404(Stage, pk=test_stage.id)

        self.assertEqual(db_test_stage.label, test_stage.label)

