from django.urls import path

import home.views

urlpatterns = [
    path('', home.views.index, name='home_route'),
    path('pricing', home.views.pricing, name='pricing_route'),
    path('profile/', home.views.user_profile, name='user_profile_route'),
]
