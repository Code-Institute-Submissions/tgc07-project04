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
        submitted_form = Task(request.POST)

        if submitted_form.is_valid():
            model = submitted_form.save()
            messages.add_message(request, messages.SUCCESS, f"Team \
                {submitted_form.cleaned_data['team_name']} has been created")
            return redirect(reverse('home_route'))
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
