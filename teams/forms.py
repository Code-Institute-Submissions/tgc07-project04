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
        teams = Team.objects.filter(team_name__icontains=data)
        if teams.count() > 0:
            raise ValidationError("A team with this name already exists.")
        if not re.search('^[a-z]\w{3}', data):
            raise ValidationError("Team name must start with a letter and \
                must contain at least 4 characters.")
        return data

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        exclude = ["team"]
