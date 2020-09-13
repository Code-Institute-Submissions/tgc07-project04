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

@login_required
def update_membership(request, team_id, membership_id):
    team = get_object_or_404(Team, pk=team_id)
    membership_to_update = get_object_or_404(Membership, pk=membership_id)

    # Get user_id relating to membership being updated
    membership_user_id = membership_to_update.user.id
    
    if request.method == "POST":
        submitted_form = MembershipForm(
            request.POST, instance=membership_to_update)
        if submitted_form.is_valid():
            membership_model = submitted_form.save(commit=False)
            membership_model.team = team

            # Count number of admin users in team from database
            admin_users = Membership.objects.filter(team=team_id).filter(
                is_admin=True)
            admin_count = admin_users.count()

            # Initialise state variable
            is_user_in_membership_table = False
            # If user membership being updated is an admin user of team
            for user in admin_users:
                if user.user.id==membership_user_id:
                    is_user_in_membership_table = True

            # If is_admin NOT checked on submitted form
            # AND user relating to membership being updated is_admin
            # AND admin_count<=1, then error
            if (not membership_model.is_admin) and (
                is_user_in_membership_table) and (admin_count<=1):
                messages.add_message(request, messages.WARNING, "Sorry, you \
                    must have at least 1 admin user in the team")
                return render(request, "teams/update-membership.html", {
                    'form': submitted_form,
                    'team': team
                })
            else:
                try:
                    # Try to create membership
                    membership_model.save()
                    messages.add_message(
                        request, messages.SUCCESS, f"Membership \
                        with {membership_model.team} has been updated")
                    return redirect(reverse('home_route'))
                except IntegrityError:
                    # If error (e.g. unique constraint failed) then flash message
                    messages.add_message(
                        request, messages.WARNING, f"Membership with \
                            {membership_model.team} already exists. Please \
                            select another user.")
                    return render(request, "teams/update-membership.html", {
                        'form': submitted_form,
                        'team': team
                    })
        else:
            return render(request, "teams/update-membership.html", {
                'form': submitted_form,
                'team': team
            })

    # request.method == "GET"
    else:
        form = MembershipForm(instance=membership_to_update)
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # If match found and current user is_admin
        if db_membership and db_membership[0].is_admin:
            return render(request, 'teams/update-membership.html', {
                'form': form,
                'team': team
            })
        # If no matches, or current user is not admin
        else:
            messages.add_message(request, messages.WARNING, "Sorry, you do \
                not have the necessary access rights to view that page")
            return redirect(reverse('account_login'))

@login_required
def delete_membership(request, team_id, membership_id):
    team = get_object_or_404(Team, pk=team_id)
    membership_to_delete = get_object_or_404(Membership, pk=membership_id)

    if request.method == "POST":
        # If number of admin users in team from database <= 1
        # AND user of membership being deleted is_admin, don't delete
        if (Membership.objects.filter(team=team_id).filter(
            is_admin=True).count() <= 1) and membership_to_delete.is_admin:
                messages.add_message(request, messages.WARNING, "Sorry, you \
                    must have at least 1 admin user in the team")
                return redirect(reverse('delete_membership_route', kwargs={
                    'team_id': team_id,
                    'membership_id': membership_id
                }))
        else:
            membership_to_delete = get_object_or_404(
                Membership, pk=membership_id)
            membership_to_delete.delete()
            messages.add_message(
                request, messages.SUCCESS, "Membership deleted")
            return redirect(reverse('home_route'))
    else:
        form = MembershipForm(instance=membership_to_delete)
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # If match found and current user is_admin
        if db_membership and db_membership[0].is_admin:
            return render(request, 'teams/delete-membership.html', {
                'form': form,
                'membership': membership_to_delete
            })
        # If no matches, or current user is not admin
        else:
            messages.add_message(request, messages.WARNING, "Sorry, you do \
                not have the necessary access rights to view that page")
            return redirect(reverse('account_login'))
