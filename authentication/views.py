from django.shortcuts import render


def login(request):
    print request
    return render(request, "registration/login.html", {
        'ceva': 'get'
    })
