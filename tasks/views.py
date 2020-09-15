from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

from .forms import *
from .models import *
from teams.models import *



################## TEST vanilla API ##################
from django.middleware.csrf import get_token
# csrf_token = get_token(request)
# csrf_token_html = '<input type="hidden" name="csrfmiddlewaretoken" value="{}" />'.format(csrf_token)
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
def api_vanilla_get(request):
    tasks = Task.objects.all()
    serialized = list(tasks.values())
    return JsonResponse(serialized, safe=False)
@csrf_exempt
def api_vanilla_post(request):
    if request.method == "POST":
        print("POST request received")
        return JsonResponse({"response": "POST"}, safe=False)

################## TEST Django REST framework ##################
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serialisers import TaskSerialiser
# All tasks
@api_view(['GET'])
def api_framework_get(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serialiser = TaskSerialiser(tasks, many=True)
        return Response(serialiser.data)
# Create task
@api_view(['POST'])
def api_framework_post(request):
	serialiser = TaskSerialiser(data=request.data)
	if serialiser.is_valid():
		serialiser.save()
	return Response(serialiser.data)
# Update whole task
@api_view(['PUT'])
def api_framework_put(request, task_id):
	task = Task.objects.get(id=task_id)
	serialiser = TaskSerialiser(instance=task, data=request.data)
	if serialiser.is_valid():
		serialiser.save()
	return Response(serialiser.data)
# Update part task MANUAL
# @api_view(['PATCH'])
# def api_framework_patch(request, task_id, new_stage_id):
#     task = Task.objects.get(id=task_id)
#     new_stage = Stage.objects.get(id=new_stage_id)
#     task.stage = new_stage
#     task.save()
#     return JsonResponse({"response": "PATCH"}, safe=False)
# Update part task SERIALISER
@api_view(['PATCH'])
def api_framework_patch(request, task_id):
    task = Task.objects.get(id=task_id)
    serialiser = TaskSerialiser(task, data=request.data, partial=True)
    if serialiser.is_valid():
        serialiser.save()
        return Response(serialiser.data)
    return JsonResponse({"response":"wrong parameters"})









# @login_required
def tasks_team(request, team_id):
    if request.method == "POST":
        return redirect(reverse('tasks_team_route'))
    else:
        tasks = {}
        tasks_team = Task.objects.filter(team=team_id)
        stages =  Stage.objects.all()
        for stage in stages:
            tasks.update({
                stage.id: {
                    'stage_label': stage.label,
                    'tasks': tasks_team.filter(
                        stage=stage.id)
                }
            })
        return render(request, 'tasks/tasks-team.html', {
            'tasks': tasks
        })

@login_required
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

    # GET method requests
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

@login_required
def update_task(request, team_id, task_id):
    team = get_object_or_404(Team, pk=team_id)
    task_to_update = get_object_or_404(Task, pk=task_id)
    task_creator = task_to_update.task_creator

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task_to_update)
        if form.is_valid():
            model = form.save(commit=False)
            model.team = team
            model.task_creator = task_creator
            model.save()
            # Save first before adding ManyToMany entries because need id
            for assignee in form.cleaned_data.get('assignee').all():
                model.assignee.add(assignee)
            messages.add_message(request, messages.SUCCESS, f"Task \
                {form.cleaned_data['title']} has been updated")
            return redirect(reverse(
                'update_task_route', kwargs={
                    'team_id': team_id,
                    'task_id': task_id
            }))
        else:
            return render(request, "tasks/update-task.html", {
                'form': form
            })

    # GET method requests
    else:
        form = TaskForm(instance=task_to_update)
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # Check if user is task_creator or is_admin of team
        if task_to_update.task_creator==request.user or (
            db_membership and db_membership[0].is_admin):
            # If current user is_admin
            if db_membership and db_membership[0].is_admin:
                # Filter assignee list by members of team
                form.fields['assignee'].queryset = User.objects.filter(
                    user_membership__team=team_id)
                return render(request, 'tasks/update-task.html', {
                    'form': form
                })
            # If current user is a member, but NOT admin
            else:
                # Only show self in list of assignees
                form.fields['assignee'].queryset = User.objects.filter(
                    id=request.user.id)
                return render(request, 'tasks/update-task.html', {
                    'form': form
                })
        # If not member, redirect
        else:
            messages.add_message(request, messages.WARNING, "Sorry, you do \
                not have the necessary access rights to view that page")
            return redirect(reverse('account_login'))

@login_required
def delete_task(request, team_id, task_id):
    task_to_delete = get_object_or_404(Task, pk=task_id)
    
    if request.method == "POST":
        task_to_delete.delete()
        messages.add_message(
            request, messages.SUCCESS, "Task deleted")
        return redirect(reverse('home_route'))
    else:
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # If current user task_creator or is_admin of team
        if task_to_delete.task_creator==request.user or (
            db_membership and db_membership[0].is_admin):
            return render(request, 'tasks/delete-task.html', {
                'task': task_to_delete
            })
        else:
            messages.add_message(request, messages.WARNING, "Sorry, you do \
                not have the necessary access rights to view that page")
            return redirect(reverse('account_login'))
