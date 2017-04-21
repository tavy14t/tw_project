from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import User


def login(request):
    return render(request, "registration/login.html", {
    })


def register(request):
    if request.method == 'POST':
        form = User(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = User()

    return render(request, 'registration/register.html', {'form': form})
