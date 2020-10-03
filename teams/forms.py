from django import forms
from django.core.exceptions import ValidationError
import re

from .models import *

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]
    
    def clean_team_name(self):
        data = self.cleaned_data['team_name']
        teams = Team.objects.filter(team_name=data)
        if teams.count() > 0:
            raise ValidationError("A team with this name already exists.")
        if not re.search('^[a-z]\w{3,}', data):
            raise ValidationError("Team name must start with a letter, \
                must contain only lower case letters, numbers or underscores \
                    and be at least 4 characters long.")
        return data

class MembershipForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=100, required=True)
    is_admin = forms.BooleanField(required=False)
