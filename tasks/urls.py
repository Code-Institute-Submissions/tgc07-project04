from django.urls import path

import tasks.views

urlpatterns = [
    path('<team_id>/team/', tasks.views.tasks_team, name='tasks_team_route'),
    path('<team_id>/team/<task_id>/', tasks.views.view_single_task,
        name='task_single_route'),
    path('<team_id>/create-task/', tasks.views.create_task,
        name='create_task_route'),
    path('<team_id>/update-task/<task_id>/', tasks.views.update_task,
        name='update_task_route'),
    path('<team_id>/delete-task/<task_id>/', tasks.views.delete_task,
        name='delete_task_route'),
    
    # API
    path('api/<team_id>/<task_id>/update-task-stage/', tasks.views.api_task_patch),
]
