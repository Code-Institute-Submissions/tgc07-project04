from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

from .forms import *
from .models import *

@login_required
def create_team(request):
    if request.method == "POST":
        submitted_form = TeamForm(request.POST)

        if submitted_form.is_valid():
            team_model = submitted_form.save()
            membership_model = Membership(
                user = request.user,
                team = team_model,
                is_admin = True
            )
            membership_model.save()
            messages.add_message(request, messages.SUCCESS, f"Team \
                {submitted_form.cleaned_data['team_name']} has been created")
            return redirect(reverse('home_route'))
        else:
            return render(request, "teams/create-team.html", {
                'form': submitted_form
            })
    else:
        form = TeamForm()
        return render(request, 'teams/create-team.html', {
            'form': form
        })

@login_required
def update_team(request, team_id):
    team_to_update = get_object_or_404(Team, pk=team_id)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team_to_update)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Updated team \
                name to {form.cleaned_data['team_name']}")
            return redirect(reverse('home_route'))
        else:
            return render(request, 'teams/update-team.html', {
                'form': form
            })
    
    else:
        form = TeamForm(instance=team_to_update)
        return render(request, 'teams/update-team.html', {
            'form': form
        })

@login_required
def delete_team(request, team_id):
    if request.method == "POST":
        team_to_delete = get_object_or_404(Team, pk=team_id)
        team_to_delete.delete()
        return redirect(reverse('home_route'))
    else:
        team_to_delete = get_object_or_404(Team, pk=team_id)
        return render(request, 'teams/delete-team.html', {
            'team': team_to_delete
        })

@login_required
def create_membership(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    if request.method == "POST":
        submitted_form = MembershipForm(request.POST)

        if submitted_form.is_valid():
            membership_model = submitted_form.save(commit=False)
            membership_model.team = team
            try:
                # Try to create membership
                membership_model.save()
                messages.add_message(request, messages.SUCCESS, f"Membership \
                    with {membership_model.team} has been created")
                return redirect(reverse('home_route'))
            except IntegrityError:
                # If error (e.g. unique constraint failed) then flash message
                messages.add_message(request, messages.WARNING, f"Membership \
                    with {membership_model.team} already exists. Please \
                        select another user.")
                return render(request, "teams/create-membership.html", {
                    'form': submitted_form,
                    'team': team
                })
        else:
            return render(request, "teams/create-membership.html", {
                'form': submitted_form,
                'team': team
            })
    else:
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # If match found and current user is_admin
        if db_membership and db_membership[0].is_admin:
            form = MembershipForm()
            return render(request, 'teams/create-membership.html', {
                'form': form,
                'team': team
            })
        # If no matches, or current user is not admin
        else:
            messages.add_message(request, messages.WARNING, "Sorry, you do \
                not have the necessary access rights to view that page")
            return redirect(reverse('account_login'))
