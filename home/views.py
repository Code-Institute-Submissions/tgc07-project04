from django.shortcuts import render

from tasks.models import *

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

