from rest_framework import serializers

from .models import *

class TaskSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ChecklistItemCreateSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['item']

class ChecklistItemSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = '__all__'
