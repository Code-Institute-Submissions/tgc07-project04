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
        submitted_form = TaskForm(request.POST)

        if submitted_form.is_valid():
            model = submitted_form.save(commit=False)
            model.team = get_object_or_404(Team, pk=team_id)
            model.task_creator = request.user
            model.save()
            # Save first before adding ManyToMany entries because need id
            for assignee in submitted_form.cleaned_data.get('assignee').all():
                model.assignee.add(assignee)
            messages.add_message(request, messages.SUCCESS, f"Task \
                {submitted_form.cleaned_data['title']} has been created")
            return redirect(reverse(
                'create_task_route', kwargs={'team_id':team_id}))
        else:
            return render(request, "tasks/create-task.html", {
                'form': submitted_form
            })
    else:
        form = TaskForm()
        # Filter assignee list by members of team
        form.fields['assignee'].queryset = User.objects.filter(
            user_membership__team=team_id)
        return render(request, 'tasks/create-task.html', {
            'form': form
        })
