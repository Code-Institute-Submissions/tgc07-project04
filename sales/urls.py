from django.urls import path

import sales.views

urlpatterns = [
    path('subscription/<team_id>', sales.views.select_subscription,
        name='checkout_select_subscription_route'),
]
