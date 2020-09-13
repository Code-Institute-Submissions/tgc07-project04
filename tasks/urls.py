from django.urls import path

import tasks.views

urlpatterns = [
    path('<team_id>/create-task/', tasks.views.create_task, name='create_task_route'),
]
