# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import json
from common import commonviews
from authentication.login_decorator import custom_login_required


@custom_login_required
def home_view(request):
    context = dict()
    context.update(commonviews.side_menu('Home'))
    return render(request, 'home.html', context)


def post(request):
    if request.method == 'GET':
        context = dict()
        context.update(commonviews.side_menu('Home'))

        print('[debug][account] context = ')
        print(json.dumps(context, indent=4))
        return render(request, 'post.html', context)
    else:
        print request
