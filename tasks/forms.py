from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

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
        exclude = ['team', 'task_creator',]
    
    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) < 2:
            raise ValidationError("Please input at least 2 characters")
        return data

class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = "__all__"

class FilterTasksForm(forms.Form):
    search_terms = forms.CharField(max_length=100, required=False)
    priority_level = forms.ModelChoiceField(
        queryset=PriorityLevel.objects.all(), required=False)
    severity_level = forms.ModelChoiceField(
        queryset=SeverityLevel.objects.all(), required=False
    )
    assignee = forms.ModelChoiceField(
        queryset=User.objects.all(), required=False
    )    
