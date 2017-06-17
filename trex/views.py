from random import shuffle

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
from controller import *
from forms import AvatarForm
from login_decorator import login_required


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
        print request.session.keys()
        code = request.GET.get('code', '')
        if len(code) != 0:
            print 'Got in here'
            res_access_token = get_feedly_client().get_access_token(settings.FEEDLY_REDIRECT_URL, code)
            request.session['feedly'] = {}
            request.session['feedly']['access_token'] = res_access_token['access_token']
            request.session['feedly']['id'] = res_access_token['id']
            request.session.modified = True
        print request.session.keys()
        return render(request, 'about.html')


@login_required
def account_settings(request):
    preferences = get_preferences(request)
    avatar_form = AvatarForm()
    context = {'preferences': preferences, 'avatar_form': avatar_form,
               'userid': request.session['userid'],
               'pocket': 1 if 'pocket' in request.session else 0,
               'feedly': 1 if 'feedly' in request.session else 0,
               'vimeo': 1 if 'vimeo' in request.session else 0}
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


########################################################################################################################
@login_required
def get_prefered(request):
    api_data = cache.get('api_data')
    if not api_data:
        api_data = get_api_data(request)
        cache.set('api_data', api_data)
    content = []
    for api in api_data:
        for post in api_data[api]['recommended']:
            try:
                api_data[api]['recommended'][post]['tags'] = [str(x) for x in
                                                              api_data[api]['recommended'][post]['tags']]
            except:
                continue
            content.append({
                'postid': post,
                'api': api,
                'title': api_data[api]['recommended'][post]['name'],
                'author': api_data[api]['recommended'][post]['uploader'],
                'author_ref': 'https://' + api_data[api]['recommended'][post]['uploader']
                if (api_data[api]['recommended'][post]['uploader'].startswith("www")
                    or api_data[api]['recommended'][post]['uploader'].endswith(".com"))
                else '/prefered?author=' + api_data[api]['recommended'][post]['uploader'],
                'tags': api_data[api]['recommended'][post]['tags'],
                'ref': api_data[api]['recommended'][post]['embed_link']
            })
    shuffle(content)
    content = {'content': content}
    return render(request, 'prefered.html', content)


@login_required
def search(request):
    if request.method == 'GET':
        return render(request, 'search.html')
    elif request.method == 'POST':
        if 'author' in request.POST:
            uploader_string = str(request.POST['author']).lower()
        else:
            uploader_string = ''
        if 'title' in request.POST:
            title_string = request.POST['title'].lower()
        else:
            title_string = ''
        if 'tags' in request.POST:
            tags_string = request.POST['tags']
            tags_list = [''.join(str(x).split()).lower() for x in tags_string.strip().split(',')]
        else:
            tags_list = []
        api_data = cache.get('api_data')
        if not api_data:
            api_data = get_api_data(request)
            cache.set('api_data', api_data)
        content = []
        for api in api_data:
            for post in api_data[api]['recommended']:
                try:
                    api_data[api]['recommended'][post]['tags'] = [str(x) for x in
                                                                  api_data[api]['recommended'][post]['tags']]
                except:
                    continue
                if title_string not in api_data[api]['recommended'][post]['name'].lower():
                    continue
                if uploader_string not in api_data[api]['recommended'][post]['uploader'].lower():
                    continue
                if not set(tags_list).issubset(set(api_data[api]['recommended'][post]['tags'])):
                    continue
                content.append({
                    'postid': post,
                    'api': api,
                    'title': api_data[api]['recommended'][post]['name'],
                    'author': api_data[api]['recommended'][post]['uploader'],
                    'author_ref': 'https://' + api_data[api]['recommended'][post]['uploader']
                    if (api_data[api]['recommended'][post]['uploader'].startswith("www")
                        or api_data[api]['recommended'][post]['uploader'].endswith(".com"))
                    else '/prefered?author=' + api_data[api]['recommended'][post]['uploader'],
                    'tags': api_data[api]['recommended'][post]['tags'],
                    'ref': api_data[api]['recommended'][post]['embed_link']
                })
        shuffle(content)
        content = {'content': content}
        return render(request, 'prefered.html', content)


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


@login_required
def pocket_login(request):
    if 'pocket' not in request.session:
        if 'pocket_request_token' not in request.session:
            request.session['pocket_request_token'] = Pocket.get_request_token(
                consumer_key=settings.POCKET_CONSUMER_KEY,
                redirect_uri=settings.POCKET_REDIRECT_URL)
            pocket_auth_url = Pocket.get_auth_url(code=request.session['pocket_request_token'],
                                                  redirect_uri=settings.POCKET_REDIRECT_URL)
            return HttpResponseRedirect(pocket_auth_url)
        try:
            print "trying to add pocket"
            user_credentials = Pocket.get_credentials(consumer_key=settings.POCKET_CONSUMER_KEY,
                                                      code=request.session['pocket_request_token'])
            print "added pocket token"
            request.session['pocket'] = user_credentials['access_token']
            request.session.modified = True
            return HttpResponseRedirect('/home/account_settings')
        except:
            return HttpResponseRedirect('/home/account_settings')
    else:
        return HttpResponseRedirect('/home/account_settings')


@login_required
def feedly_login(request):
    if 'feedly' not in request.session:
        feedly = get_feedly_client()
        code_url = feedly.get_code_url(settings.FEEDLY_REDIRECT_URL)
        return HttpResponseRedirect(code_url)
    else:
        return HttpResponseRedirect('/home/account_settings')


@login_required
def vimeo_login(request):
    if 'vimeo' not in request.session:
        vimeo_client = vimeo.VimeoClient(
            key=settings.VIMEO_CLIENT_ID,
            secret=settings.VIMEO_CLIENT_SECRET)

        # You should retrieve the "code" from the URL string Vimeo redirected to. Here, that's named `CODE_FROM_URL`.
        try:
            code = request.GET.get('code', '')
            token, user, scope = vimeo_client.exchange_code(code, settings.VIMEO_REDIRECT_URL)
            request.session['vimeo'] = token
            request.session.modified = True
            return HttpResponseRedirect('/home/account_settings')
        except vimeo.auth.GrantFailed:
            code_url = vimeo_client.auth_url(['public', 'private'], settings.VIMEO_REDIRECT_URL, None)
            return HttpResponseRedirect(code_url)
    else:
        return HttpResponseRedirect('/home/account_settings')


@login_required
def update(request):
    api_data = get_api_data(request)
    cache.set('api_data', api_data)
    return HttpResponseRedirect('/home/account_settings')
