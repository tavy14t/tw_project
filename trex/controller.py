import re
import hashlib
import cx_Oracle
from django.db import connection
from enum import Enum
from restapi.models import Comments, Posts, Users

mail_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
phone_regex = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"  # noqa


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
    INSERT_FAILED = 4,
    INVALID_EMAIL_FORMAT = 5,
    EMAIL_TOO_LONG = 6


class AccountSettingsRC(Enum):
    INVALID_JSON = 1,
    INVALID_OLD_PASSWORD = 2,
    INVALID_EMAIL_FORMAT = 3,
    INVALID_PHONE_FORMAT = 4,
    SUCCESS = 5,
    INTERNAL_SERVER_ERROR = 6,
    ADDRESS_TOO_LONG = 7,
    PHONE_TOO_LONG = 8,
    EMAIL_TOO_LONG = 9


class AccountPreferencesRC(Enum):
    SUCCESS = 1


class AddCommentRC(Enum):
    SUCCESS = 1,
    EMPTY_TEXT = 2,
    INVALID_FORM = 3


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

    cursor = connection.cursor()
    cursor.execute("insert into users (FIRSTNAME, LASTNAME, "
                   "EMAIL, PASSWORDHASH, ISACTIVATED, ROLE) values"
                   "(:fname, :lname, :email, :md5pass, 0, 'user')",
                   {'fname': firstname, 'lname':
                    lastname, 'email': email, 'md5pass': password_hash})
    cursor.close()

    cursor = connection.cursor()
    cursor.execute('select * from users where email = :mail', {'mail': email})

    for line in cursor:
        print("[debug][create_account] User with email='{}' was created!"
              .format(email))
        return RegisterRC.SUCCESS

    print("[debug][create_account] User with email='{}' was not created!"
          .format(email))
    return RegisterRC.INSERT_FAILED


def save_account_settings(request):

    def is_valid_form(request):
        if 'cur_password' not in request.POST:
            return False
        if 'new_password' not in request.POST:
            return False
        if 'phone' not in request.POST:
            return False
        if 'email' not in request.POST:
            return False
        if 'address' not in request.POST:
            return False
        return True

    def is_valid_old_password_hash(old_password_hash):
        cursor = connection.cursor()
        cursor.execute("select * from users where PASSWORDHASH = :md5pass",
                       {'md5pass': old_password_hash})

        for line in cursor:
            cursor.close()
            return True

        cursor.close()
        return False

    if not is_valid_form(request):
        return AccountSettingsRC.INVALID_JSON

    email = request.POST['email'].encode('utf8')
    cur_password = request.POST['cur_password'].encode('utf8')
    new_password = request.POST['new_password'].encode('utf8')
    phone = request.POST['phone'].encode('utf8')
    address = request.POST['address'].encode('utf8')

    cur_password_hash = get_hash(cur_password)
    old_password_hash = get_hash(new_password)

    if not re.match(mail_regex, email):
        return AccountSettingsRC.INVALID_EMAIL_FORMAT

    if not is_valid_old_password_hash(old_password_hash):
        return AccountSettingsRC.INVALID_OLD_PASSWORD

    if len(address) > 128:
        return AccountSettingsRC.ADDRESS_TOO_LONG

    if len(phone) > 16:
        return AccountSettingsRC.PHONE_TOO_LONG

    if len(email) > 128:
        return AccountSettingsRC.EMAIL_TOO_LONG

    if not re.match(phone_regex, phone):
        return AccountSettingsRC.INVALID_PHONE_FORMAT

    try:
        cursor = connection.cursor()
        cursor.execute("update users set EMAIL = :email,"
                       "PASSWORDHASH = :md5pass,"
                       "ADDRESS = :address,"
                       "PHONE = :phone"
                       "where userid = :userid",
                       {'email': email,
                        'md5pass': cur_password_hash,
                        'address': address,
                        'phone': phone,
                        'userid': request.session['userid']
                        })
        cursor.close()
        return AccountSettingsRC.SUCCESS
    except Exception:
        return AccountSettingsRC.INTERNAL_SERVER_ERROR


def get_preferences(request):
    cursor = connection.cursor()
    cursor.execute("select tagid, name from tags")
    preferences = {}

    for item in cursor:
        preferences[item[1]] = {'checked': 0, 'tagid': item[0]}

    cursor.execute("select tags.name, tags.tagid from users join users_tags "
                   "on users.userid = users_tags.userid and users.userid = "
                   "" + str(request.session['userid']) +
                   " join tags on tags.tagid = users_tags.tagid;")

    for item in cursor:
        preferences[item[0]]['checked'] = 1

    cursor.close()
    return preferences


def save_preferences(request):
    tags = request.POST.getlist('checks[]')

    cursor = connection.cursor()
    cursor.execute("delete from users_tags where "
                   "userid = " + str(request.session['userid']))

    for idx in tags:
        cursor.execute("insert into users_tags (userid, tagid)"
                       " values( :userid, :tagid )", {
                           'userid': request.session['userid'],
                           'tagid': idx
                       })
    cursor.close()


def add_comment(request, postid):
    text = ''
    if 'comment' not in request.POST:
        return AddCommentRC.INVALID_FORM

    text = request.POST['comment']
    if text == '':
        return AddCommentRC.EMPTY_TEXT

    userid = request.session['userid']
    comment = Comments.objects.create(
        userid=userid,
        postid=postid,
        text=text
    )
    comment.save()

    return AddCommentRC.SUCCESS


def get_post_content(request, postid):
    post = Posts.objects.get(postid=postid)
    comments = Comments.objects.filter(postid=postid)
    content = dict()

    content['title'] = post.title
    content['text'] = post.body

    content['comments'] = []
    for obj in comments:
        user = Users.objects.get(userid=obj.userid)
        content['comments'].append((
            obj.text, user.firstname, user.lastname
        ))

    return content


def get_all_posts(request):
    posts = Posts.objects.all()
    content = []

    for post in posts:
        author = Users.objects.filter(userid=post.userid).first()

        content.append({
            'title': post.title,
            'userid': post.userid,
            'author': author.firstname + ' ' + author.lastname,
            'postid': post.postid
        })
    return content
