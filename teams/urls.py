from django.urls import path

import teams.views

urlpatterns = [
    path('create-team/', teams.views.create_team, name='create_team_route'),
    path('<team_id>/update-team/', teams.views.update_team,
        name="update_team_route"),
    path('<team_id>/delete-team/', teams.views.delete_team,
        name="delete_team_route"),
    path('<team_id>/create-membership/', teams.views.create_membership,
        name='create_membership_route'),
    path('<team_id>/update-membership/<membership_id>',
        teams.views.update_membership, name="update_membership_route"),
    path('<team_id>/delete-membership/<membership_id>',
        teams.views.delete_membership, name="delete_membership_route"),
]
