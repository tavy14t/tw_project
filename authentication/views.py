from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from forms import UserForm, AuthForm
from django.db import connection
import cx_Oracle
from models import Users
from common import commonviews
from authentication.login_decorator import custom_login_required
import hashlib


def is_logged_in(request):
    if 'userid' in request.session.keys():
        return True
    return False


def get_hash(password):
    md5_hasher = hashlib.md5()
    md5_hasher.update(password)
    password_hash = md5_hasher.hexdigest()
    return password_hash


def authenticate_user(request, form):
    email = form.cleaned_data['email'].encode('utf8')
    password = form.cleaned_data['password'].encode('utf8')
    password_hash = get_hash(password)
    print("[debug][autheticate_user] email='{}'; password='{}'; hash='{}'".format(email, password, password_hash))

    cursor = connection.cursor()
    cursor.execute('select * from users where email = :mail', {'mail': email})

    for line in cursor:
        if line[4] == password_hash:
            request.session['userid'] = str(line[0])
            return True

        return False

    return False


def login(request):
    if is_logged_in(request):
        print '[debug][login] User is already logged in!'
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = AuthForm(request.POST)

        if form.is_valid():
            if not authenticate_user(request, form):
                messages.error(request, 'Login Failed!')
            else:
                messages.info(request, 'Login Succesfull!')

            return render(request, 'registration/login.html', {'form': form})
    else:
        form = AuthForm()

    return render(request, 'registration/login.html', {'form': form})


def logout(request):
    if is_logged_in(request):
        request.session.pop('userid', None)

    return HttpResponseRedirect('/login/')


def create_account(form):
    firstname = form.cleaned_data['firstname'].encode('utf8')
    lastname = form.cleaned_data['lastname'].encode('utf8')
    email = form.cleaned_data['mail'].encode('utf8')
    password = form.cleaned_data['password'].encode('utf8')
    password_hash = get_hash(password)
    print("[debug][create_account] firstname='{}'; lastname='{}'; email='{}'; password='{}'; hash='{}'"
          .format(firstname, lastname, email, password, password_hash))

    cursor = connection.cursor()
    cursor.execute('select * from users where email = :mail', {'mail': email})

    for line in cursor:
        print "[debug][create_account] User with mail='{}' and id='{}' was not created!".format(email, line[0])
        return False

    uid = int(cursor.callfunc('GET_UNUSED_ID', cx_Oracle.NUMBER, ['USERS']))

    cursor = connection.cursor()
    cursor.execute("insert into users (USERID, FIRSTNAME, LASTNAME, EMAIL, PASSWORDHASH, ISACTIVATED, ROLE)"
                   "values (:userid, :fname, :lname, :email, :md5pass, 0, 'U')",
                   {'userid': uid, 'fname': firstname, 'lname': lastname, 'email': email, 'md5pass': password_hash})

    cursor.execute('select * from users where email = :mail', {'mail': email})

    for line in cursor:
        print "[debug][create_account] User with mail='{}' and id='{}' was created!".format(email, uid)
        return True

    print "[debug][create_account] User with mail='{}' and id='{}' was not created!".format(email, uid)
    return False


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            if not create_account(form):
                messages.error(request, 'Account already exists!')
            else:
                messages.info(request, 'Account has been created!')

            return render(request, 'registration/register.html',
                          {'form': form})
    else:
        form = UserForm()

    return render(request, 'registration/register.html', {'form': form})


@custom_login_required
def account(request):
    result = Users.objects.all()
    context = dict()
    context['list'] = []

    for item in result:
        context['list'].append(item.firstname)

    context.update(commonviews.side_menu('Home'))
    return render(request, 'account/account.html', context)