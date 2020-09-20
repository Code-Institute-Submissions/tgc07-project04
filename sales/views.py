from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import json
import uuid
import stripe

from teams.models import *
from .models import *

@login_required
def select_subscription(request, team_id):
    team_db = get_object_or_404(Team, pk=team_id)

    if team_db.subscription_expiry < timezone.now().date():
        reference_date = timezone.now().date()
        subscription_expired = True
    else:
        reference_date = team_db.subscription_expiry
        subscription_expired = False

    thirty_days_later = reference_date + timedelta(days=30)
    one_year_later = reference_date + timedelta(days=365)

    if request.method=='POST':
        if request.POST.get('service'):
            service_db = get_object_or_404(Service, pk=request.POST.get(
                'service'))
            new_expiry = one_year_later if service_db.id==2 else (
                thirty_days_later)
            basket = request.session.get('basket', {})
            # Overwrite basket contents with new data
            basket.update({
                'team_id': team_id,
                'team_name': team_db.team_name,
                'service_id': service_db.id,
                'service_name': service_db.service_name,
                'price': service_db.price,
                'new_expiry': new_expiry.strftime('%Y-%m-%d')
            })
            
            # Save basket back to session
            request.session['basket'] = basket

            messages.success(
                request, f'{service_db.service_name} for Team \
                    {team_db.team_name} has been selected. Redirecting to \
                        checkout.')
            return redirect(reverse('checkout_stripe_route'))
        else:
            messages.warning(
                request, 'Please select a subscription')
            return redirect(reverse('checkout_select_subscription_route',
                kwargs={'team_id':team_id}))
    
    # GET method requests
    else:
        services_all = Service.objects.all()
        service_list = []
        for service in services_all:
            service_list.append({
                'id': service.id,
                'service_name': service.service_name,
                'price': service.price,
                'service_description': service.service_description
            })
        service_list[0].update({'new_expiry': thirty_days_later})
        service_list[1].update({'new_expiry': one_year_later})
        return render(request, 'sales/select-subscription.html', {
            'team': team_db,
            'services': service_list,
            'subscription_expired': subscription_expired
        })

