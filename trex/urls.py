"""trex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/home/about')),

    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),

    url(r'^home/$', RedirectView.as_view(url='/home/about')),
    url(r'^home/about$', views.about),
    url(r'^home/account_settings$', views.account_settings),
    url(r'^home/account_preferences$', views.account_preferences)
]
