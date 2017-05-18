import re
import hashlib
from django.db import connection
from enum import Enum


class AuthRC(Enum):  # Authentication Return Codes
    INVALID_EMAIL_FORMAT = 1,
    EMAIL_TOO_LONG = 2,
    SUCCESS = 3,
    UNKNOWN_ERROR = 4,
    ALREADY_LOGGED_IN = 5


def get_hash(password):
    md5_hasher = hashlib.md5()
    md5_hasher.update(password)
    password_hash = md5_hasher.hexdigest()
    return password_hash


def authenticate_user(request):
    email = request.POST['email'].encode('utf8')
    password = request.POST['password'].encode('utf8')
    mail_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    # if not re.match(mail_regex, request.POST['email']):
    #     return AuthRC.INVALID_EMAIL

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
