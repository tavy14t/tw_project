import json

from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from login_decorator import login_required
from controller import *


def login(request):
    if 'userid' in request.session.keys():
        return HttpResponseRedirect('/home')

    elif request.method == 'POST':
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
            messages.info(request, 'Account created successfully')
        elif register_result == RegisterRC.INVALID_EMAIL_FORMAT:
            messages.error(request, 'Invalid email format!')
        elif register_result == RegisterRC.EMAIL_TOO_LONG:
            messages.error(request, 'Invalid email format!')
        return render(request, 'register.html')
    elif request.method == 'GET':
        return render(request, 'register.html')


def logout(request):
    if request.method == 'GET':
        deauth_result = deauthenticate_user(request)
        if deauth_result == DeAuthRC.NOT_LOGGED_IN:
            messages.error(request, 'Operation could not be performed!')
        elif deauth_result == DeAuthRC.SUCCESS:
            messages.info(request, 'Deauthenticate successfully')

        return HttpResponseRedirect('/login')


@login_required
def about(request):
    if request.method == 'GET':
        return render(request, 'about.html')


@login_required
def account_settings(request):
    if request.method == 'GET':
        return render(request, 'account_settings.html')
    elif request.method == 'POST':
        settings_result = save_account_settings(request)
        if settings_result == AccountSettingsRC.INVALID_JSON:
            messages.info(request, 'The form is invalid!')
        elif settings_result == AccountSettingsRC.INVALID_OLD_PASSWORD:
            messages.info(request, 'The old password is incorrect!')
        elif settings_result == AccountSettingsRC.INVALID_EMAIL_FORMAT:
            messages.info(request, 'The email format is invalid!')
        elif settings_result == AccountSettingsRC.INVALID_PHONE_FORMAT:
            messages.info(request, 'The phone format is invalid!')
        elif settings_result == AccountSettingsRC.SUCCESS:
            messages.info(request, 'Changes was saved successfully')

        return render(request, 'account_settings.html')


@login_required
def account_preferences(request):
    if request.method == 'GET':
        return redirect('/home/account_settings')
    elif request.method == 'POST':
        print json.dumps(request.POST, indent=4)
        return redirect('/home/account_settings')


# def post(request):
#     if request.method == 'GET':
#         context = dict()
#         context.update(commonviews.side_menu('Home'))

#         print('[debug][account] context = ')
#         print(json.dumps(context, indent=4))
#         return render(request, 'post.html', context)
#     else:
#         print request
