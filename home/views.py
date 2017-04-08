# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from plant.models import *
from django.conf import settings
from common import commonviews


@login_required(login_url='/login')
def home_view(request):
    """
    """
    context = {}
    context.update(commonviews.side_menu('Home'))
    return render(request, 'home/home.html', context)
