import json

from rest_framework.views import APIView
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from login_decorator import login_required
from controller import *
from forms import CommentForm, AvatarForm
import os


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
            messages.error(request, 'Unknown error has occurred!')
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
            messages.info(request, 'Deautenticate successfully')

        return HttpResponseRedirect('/login')


@login_required
def about(request):
    if request.method == 'GET':
        return render(request, 'about.html')


@login_required
def account_settings(request):
    preferences = get_preferences(request)
    avatar_form = AvatarForm()
    context = {'preferences': preferences, 'avatar_form': avatar_form,
               'userid': request.session['userid']}
    if request.method == 'GET':
        return render(request, 'account_settings.html', context=context)
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
            messages.info(request, 'Changes was saved successfully!')
        elif settings_result == AccountSettingsRC.INTERNAL_SERVER_ERROR:
            messages.info(request, 'Internal server error!')
        elif settings_result == AccountSettingsRC.ADDRESS_TOO_LONG:
            messages.info(request, 'Address is too long!')
        elif settings_result == AccountSettingsRC.PHONE_TOO_LONG:
            messages.info(request, 'Phone number is too long!')
        elif settings_result == AccountSettingsRC.EMAIL_TOO_LONG:
            messages.info(request, 'Email is too long!')

        return render(request, 'account_settings.html', context)


@login_required
def account_avatar(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/home/account_settings')
    elif request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = Avatars(url=request.FILES['url'],
                             user=Users.objects.filter(
                userid=request.session['userid']).first())
            avatar.save()
            return HttpResponseRedirect('/home/account_settings')


@login_required
def account_preferences(request):
    if request.method == 'GET':
        return HttpResponseRedirect('/home/account_settings')
    if request.method == 'POST':
        save_preferences(request)
        content = {'preferences': get_preferences(request)}
        messages.warning(request, 'Preferences updated!')
        return render(request, 'account_settings.html', content)


@login_required
def get_posts(request):
    if request.method == 'GET':
        if 'postid' not in request.GET:
            content = {'content': get_all_posts()}
            return render(request, 'posts.html', content)
    elif request.method == 'POST':
        result = add_comment(request, request.GET['postid'])
        if result == AddCommentRC.INVALID_FORM:
            messages.error(request, 'Invalid Form! Comment text not found!')
        elif result == AddCommentRC.EMPTY_TEXT:
            messages.error(request, 'The comment can not be empty!')

    content = get_post_content(request.GET['postid'])
    if content['text'].endswith("pdf"):
        return render(request, 'post.html', content)
    else:
        return render(request, 'video_post.html', content)



@login_required
def get_recommended(request):
    if request.method == 'GET':
        if 'postid' not in request.GET:
            prefs = get_preferences(request)
            tag_list = [x['tagid'] for x in filter(
                lambda x: x['checked'] == 1,
                [prefs[key] for key in prefs])]
            content = {'content': get_posts_by_tags(tag_list, False, True)}
            return render(request, 'posts.html', content)
    elif request.method == 'POST':
        result = add_comment(request, request.GET['postid'])
        if result == AddCommentRC.INVALID_FORM:
            messages.error(request, 'Invalid Form! Comment text not found!')
        elif result == AddCommentRC.EMPTY_TEXT:
            messages.error(request, 'The comment can not be empty!')

    content = get_post_content(request.GET['postid'])
    return render(request, 'post.html', content)


@login_required
def get_authors(request):
    if request.method == 'GET':
        if 'userid' in request.GET:
            userid = request.GET['userid']
        else:
            content = {'content': get_all_authors()}
            return render(request, 'authors.html', content)

    content = get_user_content(userid)
    return render(request, 'author.html', content)


@login_required
def get_filtered(request):
    if request.method == 'GET':
        content = {'tags': get_empty_tags(request)}
        return render(request, 'filtered.html', content)
    elif request.method == 'POST':
        tags = request.POST.getlist('checks[]')
        tag_list = [int(x) for x in tags]
        content = {'content': get_posts_by_tags(tag_list)}
        return render(request, 'posts.html', content)


@login_required
def get_tags(request):
    if request.method == 'GET':
        if 'tagid' in request.GET:
            tagid = int(request.GET['tagid'])
            content = {'content': get_posts_by_tags([tagid], False)}
            return render(request, 'posts.html', content)
        else:
            content = {'content': get_all_tags()}
            return render(request, 'tags.html', content)


@login_required
def chat(request):
    userid = int(request.session['userid'])

    context = get_chat_rooms_context(userid)
    return render(request, 'chat.html', context)


@login_required
def chat_friends(request):
    userid = int(request.session['userid'])

    context = get_chat_friends_context(userid)
    return render(request, 'chat.html', context)
