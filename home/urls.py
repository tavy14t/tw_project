# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

import views

urlpatterns = patterns('',
                       url(r'^$', views.home_view, name='home'),
                       )
