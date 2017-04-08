# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.conf import settings


@login_required(login_url='/login')
def home_view(request):
    """
    """
    context = {}
    return render(request, 'home/home.html', context)
