import re
import os
import hashlib
from collections import Counter

from django.db import connection
from enum import Enum
from restapi.models import *
from django.db.models import Q
from utils import get_room_id_for_2_users
from FeedlyClient import FeedlyClient
from django.conf import settings
from django.http import HttpResponse

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
            cursor.close()
            return AuthRC.SUCCESS
    cursor.close()

    return AuthRC.UNKNOWN_ERROR


def deauthenticate_user(request):
    if 'userid' not in request.session.keys():
        return DeAuthRC.NOT_LOGGED_IN
    else:
        request.session.flush()
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
                       "PHONE = :phone "
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


def get_empty_tags(request):
    cursor = connection.cursor()
    cursor.execute("select tagid, name from tags")
    tags = {}

    for item in cursor:
        tags[item[1]] = {'checked': 0, 'tagid': item[0]}

    return tags


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
    print request.POST
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


def get_post_content(postid):
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


def get_all_posts():
    posts = Posts.objects.all()
    content = []
    for post in posts:
        author = Users.objects.filter(userid=post.userid).first()
        tags = []

        cursor = connection.cursor()
        cursor.execute("select name, tags.tagid from posts_tags join tags "
                       "on tags.tagid=posts_tags.tagid "
                       "and posts_tags.postid=" +
                       str(post.postid))

        for line in cursor:
            tags.append({'name': line[0], 'tagid': line[1]})

        cursor.close()

        content.append({
            'title': post.title,
            'userid': post.userid,
            'author': author.firstname + ' ' + author.lastname,
            'postid': post.postid,
            'tags': tags
        })
    return content


def get_all_authors():
    authors = Users.objects.all()
    content = []
    for user in authors:
        publications = []
        posts = Posts.objects.filter(userid=user.userid)
        for post in posts:
            publications.append({
                'postid': post.postid,
                'title': post.title
            })
        if len(publications) > 0:
            content.append({
                'author': user.firstname + ' ' + user.lastname,
                'userid': user.userid,
                'publications': publications
            })
    return content


def get_all_tags():
    tags = Tags.objects.all()
    content = []
    for item in tags:
        posts = []
        cursor = connection.cursor()
        cursor.execute("select title, posts.postid from posts "
                       "join posts_tags on posts.postid=posts_tags.postid "
                       "and posts_tags.tagid=" + str(item.tagid))
        for line in cursor:
            posts.append({'title': line[0], 'postid': line[1]})

        content.append({
            'tagid': item.tagid,
            'name': item.name,
            'posts': posts
        })

    return content


def get_posts_by_tags(tag_list,
                      should_contain_all=True,
                      sort_by_matches=False):
    posts = Posts.objects.all()
    content = []
    for post in posts:
        author = Users.objects.filter(userid=post.userid).first()
        tags = []

        cursor = connection.cursor()
        cursor.execute("select name, tags.tagid from posts_tags join tags "
                       "on tags.tagid=posts_tags.tagid "
                       "and posts_tags.postid=" +
                       str(post.postid))

        for line in cursor:
            tags.append({'name': line[0], 'tagid': line[1]})

        cursor.close()

        ids = [tags[x]['tagid'] for x in range(len(tags))]

        if should_contain_all and not set(ids).issuperset(set(tag_list)):
            continue

        if not should_contain_all and set(ids).isdisjoint(set(tag_list)):
            continue

        content.append({
            'title': post.title,
            'userid': post.userid,
            'author': author.firstname + ' ' + author.lastname,
            'postid': post.postid,
            'tags': tags
        })

    if sort_by_matches:
        content = sorted(content,
                         key=lambda entry:
                         len(set(tag_list).intersection(set(
                             [entry['tags'][x]['tagid']
                              for x in range(len(entry['tags']))]))),
                         reverse=True)

    return content


def get_user_content(userid):
    content = dict()

    user_posts = Posts.objects.filter(userid=userid)
    content['posts'] = []  # postarile lui userid
    for post in user_posts:
        content['posts'].append({
            'title': post.title,
            'postid': post.postid,
        })

    content['tags'] = []  # preferintele userului userid
    cursor = connection.cursor()
    cursor.execute("select tags.name, tags.tagid from tags "
                   "join users_tags on tags.tagid = users_tags.tagid "
                   "where users_tags.userid=" + str(int(userid)))
    for line in cursor:
        content['tags'].append({
            'name': line[0],
            'tagid': line[1]
        })
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("select url from restapi_avatars "
                   "where user_id=" + str(int(userid)))

    for line in cursor:
        content['url'] = os.path.basename(line[0])

    if 'url' not in content:
        content['url'] = 'defaultuser.png'

    cursor.close()

    user_details = Users.objects.filter(userid=userid).first()
    content['firstname'] = user_details.firstname
    content['lastname'] = user_details.lastname
    content['email'] = user_details.email
    content['address'] = user_details.address
    content['phone'] = user_details.phone

    return content


def get_chat_friends_context(userid):
    friends = Friends.objects.filter(Q(friend1=userid) | Q(friend2=userid))

    friend_chat = []
    for obj in friends:
        a = obj.friend1
        b = obj.friend2

        if b.userid == userid:
            a, b = b, a

        name = b.email
        friend_chat.append({
            'id': get_room_id_for_2_users(a.userid, b.userid),
            'name': name,
        })

    context = {
        'friends': friend_chat,
        'userid': userid
    }

    return context


def get_chat_rooms_context(userid):
    chat_rooms = ChatRoom.objects.filter(id__lte=1000).order_by('name')
    context = {
        'rooms': chat_rooms,
        'userid': userid
    }

    return context


def get_feedly_client(token=None):
    if token:
        return FeedlyClient(token=token, sandbox=True)
    else:
        return FeedlyClient(
            client_id=settings.FEEDLY_CLIENT_ID,
            client_secret=settings.FEEDLY_CLIENT_SECRET,
            sandbox=True
        )


class HttpResponseTemporaryRedirect(HttpResponse):
    status_code = 307

    def __init__(self, redirect_to):
        HttpResponse.__init__(self)
        self['Location'] = redirect_to


def get_vimeo_data(vimeo_instance):
    data = {}
    me_albums = vimeo_instance.get('/me/albums').json()
    data['albums'] = {x['uri'].split('/')[-1]: x['name'] for x in me_albums['data']}

    tags = []
    data['posts'] = {}
    for z in vimeo_instance.get('/me/likes?filter_embeddable=true').json()['data']:
        uri = z['uri'].split('/')[-1]
        data['posts'][uri] = {}
        data['posts'][uri]['name'] = z['name']
        data['posts'][uri]['uploader'] = z['user']['name']
        data['posts'][uri]['tags'] = [tag['name'] for tag in z['tags']]
        for x in [tag['name'] for tag in z['tags']]:
            tags.append(x)
        data['posts'][uri]['embed_link'] = z['embed']['html'].split('src=', 1)[1]

    data['recommended'] = {}

    tags = sorted(tags, key=Counter(tags).get, reverse=True)
    nr_tags = 3
    for tag in tags:
        print tag
        while tag in tags:
            tags.remove(tag)
        for z in vimeo_instance.get('/tags/{}/videos?per_page=5'.format(tag)).json()['data']:
            uri = z['uri'].split('/')[-1]
            data['recommended'][uri] = {}
            data['recommended'][uri]['name'] = z['name']
            data['recommended'][uri]['uploader'] = z['user']['name']
            data['recommended'][uri]['tags'] = [tag['name'] for tag in z['tags']]
            for x in [tag['name'] for tag in z['tags']]:
                tags.append(x)
            data['recommended'][uri]['embed_link'] = z['embed']['html'].split('src=', 1)[1]
        nr_tags -= 1
        if nr_tags == 0:
            break

    print data
    return data


def get_pocket_data(pocket_instance):
    pocket_posts = pocket_instance.get(detailType='complete')[0]
    data = {'posts': {}}
    for post in pocket_posts:
        data['posts'][post] = {}
        data['posts'][post]['name'] = pocket_posts[post]['given_title']
        data['posts'][post]['embed_link'] = pocket_posts[post]['resolved_url']
        if 'tags' in pocket_posts[post]:
            data['posts'][post]['tags'] = [tag for tag in pocket_posts[post]['tags']]
        else:
            data['posts'][post]['tags'] = []
    return data























































