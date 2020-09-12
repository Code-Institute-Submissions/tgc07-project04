from django import forms

from .models import *

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_name"]

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        exclude = ["team"]
