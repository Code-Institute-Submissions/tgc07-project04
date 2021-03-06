from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import *
from .models import *
from .serialisers import *
from teams.models import *

@login_required
def tasks_team(request, team_id):
    # Query database membership matches for team_id and current user
    db_membership = Membership.objects.filter(team=team_id).filter(
        user=request.user)
    if len(db_membership):
        for membership in db_membership:
            db_membership = membership
        # Check subscription expiry of team, if expired redirect to pay
        if db_membership.team.subscription_expiry < timezone.now().date():
            messages.add_message(request, messages.ERROR, "Sorry, your \
                subscription has ended. Please subscribe again to access \
                    your tasks. Don't worry, all the past tasks have been \
                        saved.")
            return redirect(reverse('checkout_select_subscription_route',
                kwargs={'team_id':team_id}))
        # If subscription still valid, then display tasks
        else:
            # GET method requests form
            filter_form = FilterTasksForm(request.GET)
            # Only show assignees that are members of the team
            filter_form.fields['assignee'].queryset = User.objects.filter(
                user_membership__team=team_id)
            
            # Empty Query
            query = ~Q(pk__in=[])
            # Results must match team_id
            query = query & Q(team=team_id)

            if request.GET:
                # Search box Query by either title OR description
                if 'search_terms' in request.GET and (
                        request.GET['search_terms']):
                    query = query & (
                        Q(title__icontains=request.GET['search_terms']) | 
                        Q(description__icontains=request.GET['search_terms'])
                    )
                # Query by selected priority_level
                if 'priority_level' in request.GET and (
                        request.GET['priority_level']):
                    query = query & Q(
                        priority_level=request.GET['priority_level'])
                # Query by selected severity_level
                if 'severity_level' in request.GET and (
                        request.GET['severity_level']):
                    query = query & Q(
                        severity_level=request.GET['severity_level'])
                # Query by assignee
                if 'assignee' in request.GET and (
                        request.GET['assignee']):
                    query = query & Q(
                        assignee=request.GET['assignee'])
            
            tasks = {}
            tasks_team = Task.objects.filter(query)
            stages = Stage.objects.all()
            for stage in stages:
                tasks.update({
                    stage.id: {
                        'stage_label': stage.label,
                        'tasks': tasks_team.filter(
                            stage=stage.id)
                    }
                })
            return render(request, 'tasks/read-tasks-team.html', {
                'tasks': tasks,
                'membership': db_membership,
                'team_id': team_id,
                'filter_tasks_form': filter_form
            })
    # If current user is not a member of team
    else:
        messages.add_message(request, messages.WARNING, "Sorry, you do \
            not have the necessary access rights to view that page")
        return redirect(reverse('account_login'))

@login_required
def view_single_task(request, team_id, task_id):
    # Query database membership matches for team_id and current user
    db_membership = Membership.objects.filter(team=team_id).filter(
        user=request.user)
    if len(db_membership):
        for membership in db_membership:
            db_membership = membership
        # Check subscription expiry of team, if expired redirect to pay
        if db_membership.team.subscription_expiry < timezone.now().date():
            messages.add_message(request, messages.ERROR, "Sorry, your \
                subscription has ended. Please subscribe again to access \
                    this page. Don't worry, all the past tasks have been \
                        saved.")
            return redirect(reverse('checkout_select_subscription_route',
                kwargs={'team_id':team_id}))
        # If subscription still valid, then display
        else:
            task = get_object_or_404(Task, pk=task_id)
            return render(request, 'tasks/read-task-single.html', {
                'task': task,
                'membership': db_membership,
            })
    else:
        messages.add_message(request, messages.WARNING, "Sorry, you do \
            not have the necessary access rights to view that page")
        return redirect(reverse('account_login'))

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
                \"{form.cleaned_data['title']}\" has been created")
            return redirect(reverse(
                'tasks_team_route', kwargs={'team_id':team_id}))
        else:
            return render(request, "tasks/create-task.html", {
                'form': form,
                'team_id': team_id,
            })

    # GET method requests
    else:
        form = TaskForm(request.GET)
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # If match found and current user is_admin
        if len(db_membership) and db_membership[0].is_admin:
            for membership in db_membership:
                db_membership = membership
            # Check subscription expiry of team, if expired redirect to pay
            if db_membership.team.subscription_expiry < timezone.now().date():
                messages.add_message(request, messages.ERROR, "Sorry, your \
                    subscription has ended. Please subscribe again to access \
                        this page. Don't worry, all the past tasks have been \
                            saved.")
                return redirect(reverse('checkout_select_subscription_route',
                    kwargs={'team_id':team_id}))
            # If subscription still valid, then display
            else:
                # Filter assignee list by members of team
                form.fields['assignee'].queryset = User.objects.filter(
                    user_membership__team=team_id)
                return render(request, 'tasks/create-task.html', {
                    'form': form,
                    'team_id': team_id,
                })
        # If current user is a member, but NOT admin
        elif len(db_membership) and not db_membership[0].is_admin:
            for membership in db_membership:
                db_membership = membership
            # Check subscription expiry of team, if expired redirect to pay
            if db_membership.team.subscription_expiry < timezone.now().date():
                messages.add_message(request, messages.ERROR, "Sorry, your \
                    subscription has ended. Please subscribe again to access \
                        this page. Don't worry, all the past tasks have been \
                            saved.")
                return redirect(reverse('checkout_select_subscription_route',
                    kwargs={'team_id':team_id}))
            # If subscription still valid, then display
            else:
                # Only show self in list of assignees
                form.fields['assignee'].queryset = User.objects.filter(
                    id=request.user.id)
                return render(request, 'tasks/create-task.html', {
                    'form': form,
                    'team_id': team_id,
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
                \"{form.cleaned_data['title']}\" has been updated")
            return redirect(reverse(
                'task_single_route', kwargs={
                    'team_id': team_id,
                    'task_id': task_id,
            }))
        else:
            return render(request, "tasks/update-task.html", {
                'form': form,
                'team': team,
            })

    # GET method requests
    else:
        form = TaskForm(instance=task_to_update)
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # If current user is_admin
        if len(db_membership) and db_membership[0].is_admin:
            for membership in db_membership:
                db_membership = membership
            # Check subscription expiry of team, if expired redirect to pay
            if db_membership.team.subscription_expiry < timezone.now().date():
                messages.add_message(request, messages.ERROR, "Sorry, your \
                    subscription has ended. Please subscribe again to access \
                        this page. Don't worry, all the past tasks have been \
                            saved.")
                return redirect(reverse('checkout_select_subscription_route',
                    kwargs={'team_id':team_id}))
            # If subscription still valid, then display
            else:
                # Filter assignee list by members of team
                form.fields['assignee'].queryset = User.objects.filter(
                    user_membership__team=team_id)
                return render(request, 'tasks/update-task.html', {
                    'form': form,
                    'team': team,
                    'task': task_to_update,
                    'membership': db_membership,
                })
        # If current user is a member, but NOT admin
        elif len(db_membership) and not db_membership[0].is_admin:
            for membership in db_membership:
                db_membership = membership
            # Check subscription expiry of team, if expired redirect to pay
            if db_membership.team.subscription_expiry < timezone.now().date():
                messages.add_message(request, messages.ERROR, "Sorry, your \
                    subscription has ended. Please subscribe again to access \
                        this page. Don't worry, all the past tasks have been \
                            saved.")
                return redirect(reverse('checkout_select_subscription_route',
                    kwargs={'team_id':team_id}))
            # If subscription still valid, then display
            else:
                # Only show self in list of assignees
                form.fields['assignee'].queryset = User.objects.filter(
                    id=request.user.id)
                return render(request, 'tasks/update-task.html', {
                    'form': form,
                    'team': team,
                    'task': task_to_update,
                    'membership': db_membership,
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
        return redirect(reverse('tasks_team_route',
            kwargs={'team_id': team_id}))
    
    # GET method requests
    else:
        # Query database membership matches for team_id and current user
        db_membership = Membership.objects.filter(team=team_id).filter(
            user=request.user)
        # If current user task_creator or is_admin of team
        if task_to_delete.task_creator==request.user or (
            len(db_membership) and db_membership[0].is_admin):
            for membership in db_membership:
                db_membership = membership
            # Check subscription expiry of team, if expired redirect to pay
            if db_membership.team.subscription_expiry < timezone.now().date():
                messages.add_message(request, messages.ERROR, "Sorry, your \
                    subscription has ended. Please subscribe again to access \
                        this page. Don't worry, all the past tasks have been \
                            saved.")
                return redirect(reverse('checkout_select_subscription_route',
                    kwargs={'team_id':team_id}))
            # If subscription still valid, then display
            else:
                return render(request, 'tasks/delete-task.html', {
                    'task': task_to_delete
                })
        else:
            messages.add_message(request, messages.WARNING, "Sorry, you do \
                not have the necessary access rights to view that page")
            return redirect(reverse('account_login'))

@login_required
@api_view(['PATCH'])
def api_task_patch(request, team_id, task_id):
    # Query database membership matches for team_id and current user
    db_membership = Membership.objects.filter(team=team_id).filter(
        user=request.user)
    if len(db_membership):
        task = Task.objects.get(id=task_id)
        serialiser = TaskSerialiser(task, data=request.data, partial=True)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data)
        else:
            return JsonResponse({"error":"wrong parameters"})
    else:
        return JsonResponse({"error":"wrong user credentials"})

@login_required
@api_view(['POST'])
def api_create_checklist_item_post(request, team_id, task_id):
    # Query database membership matches for team_id and current user
    db_membership = Membership.objects.filter(team=team_id).filter(
        user=request.user)
    if len(db_membership):
        task = Task.objects.get(id=task_id)
        serialiser = ChecklistItemCreateSerialiser(data=request.data)
        if serialiser.is_valid():
            # Add task ForeignKey separately
            serialiser.validated_data.update({'task': task})
            serialiser.save()
            return Response(serialiser.data)
        else:
            return JsonResponse({"error":"wrong parameters"})
    else:
        return JsonResponse({"error":"wrong user credentials"})

@login_required
@api_view(['GET'])
def api_read_checklist_items_get(request, team_id, task_id):
    # Query database membership matches for team_id and current user
    db_membership = Membership.objects.filter(team=team_id).filter(
        user=request.user)
    if len(db_membership):
        checklist_items = ChecklistItem.objects.filter(task=task_id)
        serialiser = ChecklistItemSerialiser(checklist_items, many=True)
        return Response(serialiser.data)
    else:
        return JsonResponse({"error":"wrong user credentials"})

@login_required
@api_view(['PATCH'])
def api_update_checklist_item_patch(request, team_id, checklist_id):
    # Query database membership matches for team_id and current user
    db_membership = Membership.objects.filter(team=team_id).filter(
        user=request.user)
    if len(db_membership):
        checklist_item = ChecklistItem.objects.get(id=checklist_id)
        serialiser = ChecklistItemSerialiser(
            checklist_item, data=request.data, partial=True)
        if serialiser.is_valid():
            serialiser.save()
            return Response(serialiser.data)
        else:
            return JsonResponse({"error":"wrong parameters"})
    else:
        return JsonResponse({"error":"wrong user credentials"})

@login_required
@api_view(['DELETE'])
def api_delete_checklist_item(request, team_id, checklist_id):
    # Query database membership matches for team_id and current user
    db_membership = Membership.objects.filter(team=team_id).filter(
        user=request.user)
    if len(db_membership):
        checklist_item = ChecklistItem.objects.get(id=checklist_id)
        checklist_item.delete()
        return JsonResponse({"response":"deleted"})
    else:
        return JsonResponse({"error":"wrong user credentials"})

@login_required
@api_view(['GET'])
def api_count_checklist_items_get(request, team_id, task_id):
    # Query database membership matches for team_id and current user
    db_membership = Membership.objects.filter(team=team_id).filter(
        user=request.user)
    if len(db_membership):
        items_count = ChecklistItem.objects.filter(task=task_id).count()
        checked_items_count = ChecklistItem.objects.filter(task=task_id).filter(
            completed=True).count()
        return JsonResponse({
            "items_count": items_count,
            "checked_items_count": checked_items_count,
            })
    else:
        return JsonResponse({"error":"wrong user credentials"})

