from django import forms

from .models import *

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = "__all__"
