from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import User
import md5


def login(request):
    return render(request, "registration/login.html", {
    })


def register(request):
    if request.method == 'POST':
        form = User(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            mail = form.cleaned_data['mail']
            password = form.cleaned_data['password']
            md5_hasher = md5.new()
            md5_hasher.update(password)
            password = md5_hasher.digest()
            # TODO : INSERT INTO DB OR PRINT ERROR IF ACCOUNT ALREADY EXISTS!
            return HttpResponseRedirect('/thanks/')
    else:
        form = User()

    return render(request, 'registration/register.html', {'form': form})
