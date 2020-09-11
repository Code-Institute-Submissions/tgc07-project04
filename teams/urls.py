from django.urls import path

import teams.views

urlpatterns = [
    path('create/', teams.views.create_team, name='create_team_route'),
    path('update/<team_id>', teams.views.update_team,
        name="update_team_route"),
]
