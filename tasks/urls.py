from django.urls import path

import tasks.views

urlpatterns = [
    path('<team_id>/team/', tasks.views.tasks_team,
        name='tasks_team_route'),
    path('<team_id>/create-task/', tasks.views.create_task,
        name='create_task_route'),
    path('<team_id>/update-task/<task_id>/', tasks.views.update_task,
        name='update_task_route'),
    path('<team_id>/delete-task/<task_id>/', tasks.views.delete_task,
        name='delete_task_route'),
    
    # Vanilla API
    path('vanilla/api/get/', tasks.views.api_vanilla_get),
    path('vanilla/api/post/', tasks.views.api_vanilla_post),

    # Django REST framework
    path('framework/api/get/', tasks.views.api_framework_get),
    path('framework/api/patch/<task_id>', tasks.views.api_framework_patch),
]
