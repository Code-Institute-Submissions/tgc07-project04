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
    path('api/<team_id>/<task_id>/update-task-stage/',
        tasks.views.api_task_patch),
    path('api/<team_id>/<task_id>/create-checklist-item/',
        tasks.views.api_create_checklist_item_post),
    path('api/<team_id>/<task_id>/read-checklist-items/',
        tasks.views.api_read_checklist_items_get),
    path('api/<team_id>/<checklist_id>/update-checklist-item/',
        tasks.views.api_update_checklist_item_patch),
    path('api/<team_id>/<checklist_id>/delete-checklist-item/',
        tasks.views.api_delete_checklist_item),
    path('api/<team_id>/<task_id>/count-checklist-items/',
        tasks.views.api_count_checklist_items_get),
]
