from django.urls import path

import tasks.views

urlpatterns = [
    path('<team_id>/tasks/', tasks.views.all_tasks,
        name='all_tasks_route'),
    path('<team_id>/create-task/', tasks.views.create_task,
        name='create_task_route'),
    path('<team_id>/update-task/<task_id>/', tasks.views.update_task,
        name='update_task_route'),
    path('<team_id>/delete-task/<task_id>/', tasks.views.delete_task,
        name='delete_task_route'),
]
