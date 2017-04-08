from django.shortcuts import render
import django.contrib.auth.views.login


def _login(request):
    print request
    return render(request, "registration/login.html", {
        'ceva': 'get'
    })
