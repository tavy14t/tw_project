import re
import hashlib
import cx_Oracle
from django.db import connection
from enum import Enum

mail_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"


class AuthRC(Enum):  # Authentication Return Codes
    INVALID_EMAIL_FORMAT = 1,
    EMAIL_TOO_LONG = 2,
    SUCCESS = 3,
    UNKNOWN_ERROR = 4,
    ALREADY_LOGGED_IN = 5,


class DeAuthRC(Enum):  # Authentication Return Codes
    NOT_LOGGED_IN = 1,
    SUCCESS = 2


class RegisterRC(Enum):
    ALREADY_EXISTS = 1,
    SUCCESS = 2,
    INVALID_SQL_METHOD = 4,
    INSERT_FAILED = 5,
    INVALID_EMAIL_FORMAT = 6,
    EMAIL_TOO_LONG = 7


def get_hash(password):
    md5_hasher = hashlib.md5()
    md5_hasher.update(password)
    password_hash = md5_hasher.hexdigest()
    return password_hash


def authenticate_user(request):
    email = request.POST['email'].encode('utf8')
    password = request.POST['password'].encode('utf8')

    if not re.match(mail_regex, email):
        return AuthRC.INVALID_EMAIL_FORMAT

    if len(email) >= 256:
        return AuthRC.MAIL_TOO_LONG

    if 'userid' in request.session.keys():
        return AuthRC.ALREADY_LOGGED_IN

    password_hash = get_hash(password)
    print("[debug][autheticate_user] email='{}'; password='{}'; hash='{}'"
          .format(email, password, password_hash))

    cursor = connection.cursor()
    query = 'select * from users where email = :mail'
    cursor.execute(query, {'mail': email})
    for line in cursor:
        print line
        if line[4] == password_hash:
            request.session['userid'] = str(line[0])
            return AuthRC.SUCCESS
    cursor.close()

    return AuthRC.UNKNOWN_ERROR


def deauthenticate_user(request):
    if 'userid' not in request.session.keys():
        return DeAuthRC.NOT_LOGGED_IN
    else:
        request.session.pop('userid')
        return DeAuthRC.SUCCESS


def create_account(request):
    firstname = request.POST['firstname'].encode('utf8')
    lastname = request.POST['lastname'].encode('utf8')
    email = request.POST['mail'].encode('utf8')
    password = request.POST['password'].encode('utf8')
    password_hash = get_hash(password)

    print("[debug][create_account] firstname='{}'; "
          "lastname='{}'; email='{}'; password='{}'; hash='{}'"
          .format(firstname, lastname, email, password, password_hash))

    if len(email) >= 256:
        return RegisterRC.MAIL_TOO_LONG

    if not re.match(mail_regex, email):
        return RegisterRC.INVALID_EMAIL_FORMAT

    cursor = connection.cursor()
    cursor.execute('select * from users where email = :mail', {'mail': email})

    for line in cursor:
        print("[debug][create_account] User with mail='{}' "
              " and id='{}' was not created!"
              .format(email, line[0]))
        return RegisterRC.ALREADY_EXISTS

    try:
        uid = int(cursor.callfunc('GET_UNUSED_ID',
                                  cx_Oracle.NUMBER, ['USERS']))
    except Exception:
        return RegisterRC.INVALID_SQL_METHOD

    cursor = connection.cursor()
    cursor.execute("insert into users (USERID, FIRSTNAME, LASTNAME, "
                   "EMAIL, PASSWORDHASH, ISACTIVATED, ROLE) values"
                   "(:userid, :fname, :lname, :email, :md5pass, 0, 'U')",
                   {'userid': uid, 'fname': firstname, 'lname':
                    lastname, 'email': email, 'md5pass': password_hash})
    cursor.close()

    cursor = connection.cursor()
    cursor.execute('select * from users where email = :mail', {'mail': email})

    for line in cursor:
        print("[debug][create_account] User with mail='{}' "
              "and id='{}' was created!".format(email, uid))
        return RegisterRC.SUCCESS

    print("[debug][create_account] User with mail='{}' "
          "and id='{}' was not created!".format(email, uid))
    return RegisterRC.INSERT_FAILED


