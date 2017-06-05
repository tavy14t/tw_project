from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
import restapi.views
import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/home/about')),
    url(r'^admin/', admin.site.urls),

    url(r'^restapi/posts/', restapi.views.PostList.as_view()),
    url(r'^restapi/users/', restapi.views.UsersList.as_view()),

    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),

    url(r'^post/$', views.post),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^friends/$', views.chat_friends, name='chat'),

    url(r'^home/$', RedirectView.as_view(url='/home/about')),
    url(r'^home/about$', views.about),
    url(r'^home/account_settings$', views.account_settings),
    url(r'^home/account_preferences$', views.account_preferences)
]

urlpatterns = format_suffix_patterns(urlpatterns)
