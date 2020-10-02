from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from tasks.models import *
from sales.models import Service

def index(request):
    tasks = {}
    tasks_team = Task.objects.filter(team=1)
    stages = Stage.objects.all()
    for stage in stages:
        tasks.update({
            stage.id: {
                'stage_label': stage.label,
                'tasks': tasks_team.filter(
                    stage=stage.id)
            }
        })
    return render(request, 'home/index.html', {
        'tasks': tasks,
        'team_id': None,
        'demo': True
    })

def pricing(request):
    # Service subscriptions available for purchase
    services_all = Service.objects.all()
    service_list = []
    for service in services_all:
        service_list.append({
            'id': service.id,
            'service_name': service.service_name,
            'price': service.price,
            'service_description': service.service_description
        })
    return render(request, 'home/pricing.html', {'services':services_all})

@login_required
def user_profile(request):
    return render(request, 'home/user-profile.html')
