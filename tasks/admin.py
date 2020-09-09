from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Stage)
admin.site.register(PriorityLevel)
admin.site.register(SeverityLevel)
admin.site.register(Task)
admin.site.register(ChecklistItem)
admin.site.register(TaskAssignee)
