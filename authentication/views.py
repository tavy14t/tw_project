from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
import cx_Oracle
from models import Users
from common import commonviews
from authentication.login_decorator import custom_login_required

import json
from auth_controller import *


def is_logged_in(request):
    if 'userid' in request.session.keys():
        return True
    return False


def login(request):
    if request.method == 'POST':
        auth_result = authenticate_user(request)
        if auth_result == AuthRC.INVALID_EMAIL_FORMAT:
            messages.error(request, 'Invalid email format!')
        elif auth_result == AuthRC.EMAIL_TOO_LONG:
            messages.error(request, 'Email is too long!')
        elif auth_result == AuthRC.SUCCESS:
            messages.info(request, 'Login Succesfull!')
        else:
            messages.error(request, 'Unknown error has occured!')
        return render(request, 'login.html')

    return render(request, 'login.html')


def logout(request):
    if is_logged_in(request):
        request.session.pop('userid', None)

    return HttpResponseRedirect('/login/')


def create_account(form):
    pass
    # firstname = form.cleaned_data['firstname'].encode('utf8')
    # lastname = form.cleaned_data['lastname'].encode('utf8')
    # email = form.cleaned_data['mail'].encode('utf8')
    # password = form.cleaned_data['password'].encode('utf8')
    # password_hash = get_hash(password)
    # print("[debug][create_account] firstname='{}'; lastname='{}'; email='{}'; password='{}'; hash='{}'"
    #       .format(firstname, lastname, email, password, password_hash))

    # cursor = connection.cursor()
    # cursor.execute('select * from users where email = :mail', {'mail': email})

    # for line in cursor:
    #     print "[debug][create_account] User with mail='{}' and id='{}' was not created!".format(email, line[0])
    #     return False

    # uid = int(cursor.callfunc('GET_UNUSED_ID', cx_Oracle.NUMBER, ['USERS']))

    # cursor = connection.cursor()
    # cursor.execute("insert into users (USERID, FIRSTNAME, LASTNAME, EMAIL, PASSWORDHASH, ISACTIVATED, ROLE)"
    #                "values (:userid, :fname, :lname, :email, :md5pass, 0, 'U')",
    #                {'userid': uid, 'fname': firstname, 'lname': lastname, 'email': email, 'md5pass': password_hash})

    # cursor.execute('select * from users where email = :mail', {'mail': email})

    # for line in cursor:
    #     print "[debug][create_account] User with mail='{}' and id='{}' was created!".format(email, uid)
    #     return True

    # print "[debug][create_account] User with mail='{}' and id='{}' was not created!".format(email, uid)
    # return False


def register(request):
    pass
    # if request.method == 'POST':
    #     form = UserForm(request.POST)
    #     if form.is_valid():
    #         if not create_account(form):
    #             messages.error(request, 'Account already exists!')
    #         else:
    #             messages.info(request, 'Account has been created!')

    #         return render(request, 'registration/register.html',
    #                       {'form': form})
    # else:
    #     form = UserForm()

    # return render(request, 'registration/register.html', {'form': form})


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
