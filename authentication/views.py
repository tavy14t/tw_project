from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
import cx_Oracle
from models import Users
from common import commonviews
from authentication.login_decorator import custom_login_required

import json
from auth_controller import *


def login(request):
    if 'userid' in request.session.keys():
        return render(request, 'home.html')
    if request.method == 'POST':
        auth_result = authenticate_user(request)

        if auth_result == AuthRC.INVALID_EMAIL_FORMAT:
            messages.error(request, 'Invalid email format!')
        elif auth_result == AuthRC.EMAIL_TOO_LONG:
            messages.error(request, 'Email is too long!')
        elif auth_result == AuthRC.SUCCESS:
            messages.info(request, 'Login Successfully!')
        elif auth_result == AuthRC.ALREADY_LOGGED_IN:
            messages.info(request, 'Already logged in!')
        elif auth_result == AuthRC.UNKNOWN_ERROR:
            messages.error(request, 'Unknown error has occured!')
        return render(request, 'login.html')
    elif request.method == 'GET':
        print request.session
        print request.session.keys()

        return render(request, 'login.html')


def logout(request):
    if is_logged_in(request):
        request.session.pop('userid', None)

    return HttpResponseRedirect('/login/')


def register(request):
    if request.method == 'POST':
        register_result = create_account(request)
        if register_result == RegisterRC.ALREADY_EXISTS:
            messages.error(request, 'Account already exists!')
        elif register_result == RegisterRC.INVALID_SQL_METHOD:
            messages.error(request, 'Internal server error!')
        elif register_result == RegisterRC.INSERT_FAILED:
            messages.error(request, 'Account creation failed!')
        elif register_result == RegisterRC.SUCCESS:
            messages.info(request, 'Account created succefully')
        elif register_result == RegisterRC.INVALID_EMAIL_FORMAT:
            messages.error(request, 'Invalid email format!')
        elif register_result == RegisterRC.EMAIL_TOO_LONG:
            messages.error(request, 'Invalid email format!')
        return render(request, 'register.html')
    elif request.method == 'GET':
        return render(request, 'register.html')


@custom_login_required
def account(request):
    if request.method == 'GET':
        context = dict()
        context.update(commonviews.side_menu('Home'))

        print('[debug][account] context = ')
        print(json.dumps(context, indent=4))
        return render(request, 'account/account.html', context)
    else:
        print request
