# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from common import commonviews
from authentication.login_decorator import custom_login_required


@custom_login_required
def home_view(request):
    context = dict()

    context.update(commonviews.side_menu('Home'))
    return render(request, 'home/home.html', context)
