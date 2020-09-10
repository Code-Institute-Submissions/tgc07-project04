from django import forms

from .models import *

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = "__all__"

class PriorityLevelForm(forms.ModelForm):
    class Meta:
        model = PriorityLevel
        fields = "__all__"

class SeverityLevelForm(forms.ModelForm):
    class Meta:
        model = SeverityLevel
        fields = "__all__"

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = "__all__"
