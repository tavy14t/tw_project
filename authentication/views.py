from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from forms import UserForm, AuthForm
from models import Users
import md5
import cx_Oracle
from trex import settings

from login_decorator import custom_login_required


def authenticate_user(request, form):
    email = form.cleaned_data['email'].encode('utf8')
    password = form.cleaned_data['password'].encode('utf8')

    md5_hasher = md5.new()
    md5_hasher.update(password)
    password_hash = md5_hasher.hexdigest()

    print password_hash

    trex_db = settings.DATABASES['default']
    ip = trex_db['HOST']
    port = trex_db['PORT']
    SID = trex_db['NAME']
    user = trex_db['USER']
    password = trex_db['PASSWORD']
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)

    con = cx_Oracle.connect(user, password, dsn_tns)
    cursor = con.cursor()
    cursor.prepare('select * from users where email = :mail')

    cursor.execute(None, {'mail': email})

    for c in cursor:
        print c
        print password_hash

        con.close()
        if c[4] == password_hash:
            request.session['userid'] = str(c[0])
            return True

        return False

    return False


def login(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        print form

        if form.is_valid():
            if not authenticate_user(request, form):
                messages.error(request, 'Login Failed!')
            else:
                messages.info(request, 'Login Succesfull!')

            return render(request, 'registration/login.html',
                          {'form': form})
    else:
        form = AuthForm()

    return render(request, 'registration/login.html', {'form': form})


def logout(request):
    if request.method == 'POST':
        request.session.pop('userid', None)

    form = AuthForm()
    return render(request, 'registration/login.html', {'form': form})


def create_account(form):
    firstname = form.cleaned_data['firstname'].encode('utf8')
    lastname = form.cleaned_data['lastname'].encode('utf8')
    mail = form.cleaned_data['mail'].encode('utf8')
    password = form.cleaned_data['password'].encode('utf8')
    md5_hasher = md5.new()
    md5_hasher.update(password)
    password_hash = md5_hasher.hexdigest()

    trex_db = settings.DATABASES['default']
    ip = trex_db['HOST']
    port = trex_db['PORT']
    SID = trex_db['NAME']
    user = trex_db['USER']
    password = trex_db['PASSWORD']
    dsn_tns = cx_Oracle.makedsn(ip, port, SID)

    con = cx_Oracle.connect(user, password, dsn_tns)
    cursor = con.cursor()
    cursor.prepare('select * from users where email = :mail')
    cursor.execute(None, {'mail': mail})
    for line in cursor:
        con.close()
        return False

    uid = int(cursor.callfunc('GET_UNUSED_ID', cx_Oracle.NUMBER, ['USERS']))
    print 'uid', uid

    cursor.prepare(
        """
        insert into users (USERID, FIRSTNAME, LASTNAME,
        EMAIL, PASSWORDHASH, ISACTIVATED, ROLE)
        values (:userid, :fname, :lname, :email, :md5pass, 0, 'U')
        """)

    cursor.execute(None, {'userid': uid, 'fname': firstname,
                          'lname': lastname, 'email': mail,
                          'md5pass': password_hash})
    con.commit()

    cursor.prepare('select * from users where email = :mail')
    cursor.execute(None, {'mail': mail})
    for line in cursor:
        con.close()
        print 'NEW USER', mail, firstname, lastname
        return True

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
