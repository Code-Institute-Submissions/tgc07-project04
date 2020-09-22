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
        exclude = ['team', 'task_creator',]

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
