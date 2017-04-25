# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from models import Users
from common import commonviews
from authentication.login_decorator import custom_login_required


@custom_login_required
def home_view(request):
    result = Users.objects.all()
    context = dict()
    context['list'] = []

    print result

    for item in result:
        context['list'].append(item.firstname)

    context.update(commonviews.side_menu('Home'))
    return render(request, 'home/home.html', context)
