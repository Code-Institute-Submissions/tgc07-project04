from django.urls import path

import teams.views

urlpatterns = [
    path('create-team/', teams.views.create_team, name='create_team_route'),
    path('<team_id>/update-team/', teams.views.update_team,
        name="update_team_route"),
    path('<team_id>/delete-team/', teams.views.delete_team,
        name="delete_team_route"),
    path('<team_id>/purchases/', teams.views.team_transaction_history,
        name='team_transaction_history_route'),
    path('<team_id>/create-membership/', teams.views.create_membership,
        name='create_membership_route'),
    path('<team_id>/update-membership/<membership_id>/',
        teams.views.update_membership, name="update_membership_route"),
    path('<team_id>/delete-membership/<membership_id>/',
        teams.views.delete_membership, name="delete_membership_route"),
    path('memberships/team/<team_id>/', teams.views.team_memberships,
        name='team_memberships_route'),
    path('memberships/user/', teams.views.user_memberships,
        name='user_memberships_route'),
]
