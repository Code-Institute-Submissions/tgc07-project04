from django.shortcuts import render

def index(request):
    if request.user.is_authenticated:
        print(request.user.id)
        print(request.user.username)
        print(request.user.email)
    return render(request, 'home/index.html')
