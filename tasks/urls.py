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
    path('api/vanilla/get/', tasks.views.api_vanilla_get),
    path('api/vanilla/post/', tasks.views.api_vanilla_post),

    # Django REST framework
    path('api/framework/get/', tasks.views.api_framework_get),
    path('api/framework/put/<task_id>/', tasks.views.api_framework_put),
    # path('api/framework/patch/<task_id>/<new_stage_id>/', tasks.views.api_framework_patch), # MANUAL way
    path('api/<team_id>/<task_id>/update-task-stage/', tasks.views.api_update_task_stage), # SERIALISER takes JSON e.g. {"stage":"1"}
]
