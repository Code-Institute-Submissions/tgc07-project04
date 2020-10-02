from django.urls import path

import sales.views

urlpatterns = [
    path('subscription/<team_id>/', sales.views.select_subscription,
        name='checkout_select_subscription_route'),
    path('stripe/', sales.views.checkout_stripe,
        name='checkout_stripe_route'),
    path('success/', sales.views.checkout_success,
        name='checkout_success_route'),
    path('cancelled/', sales.views.checkout_cancelled,
        name='checkout_cancelled_route'),
    path('payment-completed/', sales.views.payment_completed,
        name='payment_completed_route'),
]
