# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.template import Context, loader
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from models import Users


@login_required(login_url='/login')
def home_view(request):
    # """
    # """
    result = Users.objects.all()
    context = dict()
    context['list'] = ''

    print result

    for item in result:
        context['list'] += item.name + '\n'

    context = Context(context)
    return render(request, 'home/home.html', context)
