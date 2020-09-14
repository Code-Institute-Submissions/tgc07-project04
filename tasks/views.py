from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from .forms import *
from .models import *
from teams.models import *

# @login_required
def create_task(request, team_id):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            model = form.save(commit=False)
            model.team = get_object_or_404(Team, pk=team_id)
            model.task_creator = request.user
            model.save()
            # Save first before adding ManyToMany entries because need id
            for assignee in form.cleaned_data.get('assignee').all():
                model.assignee.add(assignee)
            messages.add_message(request, messages.SUCCESS, f"Task \
                {form.cleaned_data['title']} has been created")
            return redirect(reverse(
                'create_task_route', kwargs={'team_id':team_id}))
        else:
            return render(request, "tasks/create-task.html", {
                'form': form
            })

    # request.method == "GET"
    else:
        form = TaskForm()
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # If match found and current user is_admin
        if db_membership and db_membership[0].is_admin:
            # Filter assignee list by members of team
            form.fields['assignee'].queryset = User.objects.filter(
                user_membership__team=team_id)
            return render(request, 'tasks/create-task.html', {
                'form': form
            })
        # If current user is a member, but NOT admin
        elif db_membership and not db_membership[0].is_admin:
            # Only show self in list of assignees
            form.fields['assignee'].queryset = User.objects.filter(
                id=request.user.id)
            return render(request, 'tasks/create-task.html', {
                'form': form
            })
        # If not member, redirect
        else:
            messages.add_message(request, messages.WARNING, "Sorry, you do \
                not have the necessary access rights to view that page")
            return redirect(reverse('account_login'))

