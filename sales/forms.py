from django import forms

from .models import *

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"

