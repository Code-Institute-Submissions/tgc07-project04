from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
            messages.success(
                request, f"Team {submitted_form.cleaned_data['team_name']} \
                    has been created")
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
            messages.success(
                request, f"Updated team name to \
                    {form.cleaned_data['team_name']}")
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
