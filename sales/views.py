from django.shortcuts import (render, redirect, reverse, get_object_or_404, 
    HttpResponse)
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

@login_required
def checkout_stripe(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    transaction_line_items = []
    transaction_metadata = {}

    basket = request.session.get('basket', {})
    team_db = get_object_or_404(Team, pk=basket.get('team_id'))
    service_db = get_object_or_404(Service, pk=basket.get('service_id'))
    # Create line_item
    item = {
        "name": service_db.service_name + " for team " + team_db.team_name,
        "amount": service_db.price, # Must be integer and in cents
        "quantity": 1,
        "currency": "usd"
    }

    transaction_line_items.append(item)
    transaction_metadata.update({
        'team_id': basket.get('team_id'),
        'team_name': team_db.team_name,
        'service_id': basket.get('service_id'),
        'service_name': service_db.service_name,
        'price': service_db.price,
        'new_expiry': basket.get('new_expiry'),
        'paid_by_user': request.user.id
    })

    # Get our site's domain name
    current_site = Site.objects.get_current()
    domain = current_site.domain

    # Pass line_items to stripe and in return get checkout session_id
    session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = transaction_line_items,
        client_reference_id = str(uuid.uuid4()),
        mode = 'payment',
        success_url = domain + reverse('checkout_success_route'),
        cancel_url = domain + reverse('checkout_cancelled_route'),
        metadata = {'data': json.dumps(transaction_metadata)}
    )

    # Render our template which will auto-redirect to Stripe
    return render(request, 'sales/checkout-stripe-redirect.html', {
        'session_id': session.id,
        'public_key': settings.STRIPE_PUBLISHABLE_KEY
    })

@login_required
def checkout_success(request):
    basket = request.session.get('basket', {})
    team = get_object_or_404(Team, pk=basket.get('team_id'))
    messages.add_message(request, messages.SUCCESS, f"Team \
        {team.team_name}'s subscription extended until \
            {team.subscription_expiry}. Thank you for the purchase!")
    # Empty shopping basket
    request.session['basket'] = {}
    return redirect(reverse('checkout_select_subscription_route',
        kwargs={'team_id':team.id}))

@login_required
def checkout_cancelled(request):
    basket = request.session.get('basket', {})
    team = get_object_or_404(Team, pk=basket.get('team_id'))
    messages.add_message(request, messages.ERROR, "Ooops, something went \
        wrong. Please try to make the payment again, sorry.")
    return redirect(reverse('checkout_select_subscription_route',
        kwargs={'team_id':team.id}))

@csrf_exempt
def payment_completed(request):
    # Payload represents data sent back to us by Stripe
    payload = request.body
    endpoint_secret = settings.STRIPE_WEBHOOK_SIGNING_SECRET
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(e)
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_payment(session)

    return HttpResponse(status=200)

def handle_payment(session):
    # UUID generated by us and passed to Stripe as client_reference_id
    my_transaction_ref = session.get('client_reference_id')

    # Metadata passed to Stripe by us as JSON string inside dictionary
    metadata = json.loads(session.get('metadata').get('data',{}))

    team = Team.objects.get(id=metadata.get('team_id'))
    service = Service.objects.get(id=metadata.get('service_id'))

    # Set a reference date based on later of current date or 
    # team's existing subscription expiry date
    if team.subscription_expiry > timezone.now().date():
        reference_date = team.subscription_expiry
    else:
        reference_date = timezone.now().date()

    # Calculate new subscription expiry date based on subscription purchased
    # and reference date calculated above
    if service.id == 1:
        new_subscription_expiry = reference_date + timedelta(days=30)
    elif service.id==2:
        new_subscription_expiry = reference_date + timedelta(days=365)
    else:
        new_subscription_expiry = team.subscription_expiry
    # Update database with new subscription expiry date
    team.subscription_expiry = new_subscription_expiry
    team.save()

    # Save purchase transaction data to database for accounting history
    transaction = Transaction()
    transaction.date = timezone.now().date()
    transaction.team = team
    transaction.service = service
    transaction.transaction_ref = my_transaction_ref
    transaction.stripe_webhook_id = session.get('id')
    transaction.paid_by_user = User.objects.get(id = metadata.get(
        'paid_by_user'))
    transaction.save()
