from django.conf.urls import url
from django.contrib import admin
from django.views.generic import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
import restapi.views
import views


urlpatterns = [
    url(r'^$', views.about),#RedirectView.as_view(url='/home/about')),
    url(r'^admin/', admin.site.urls),

    url(r'^restapi/posts/$', restapi.views.PostList.as_view()),
    url(r'^restapi/users/$', restapi.views.UsersList.as_view()),
    url(r'^restapi/posts/', restapi.views.get_post),

    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),

    url(r'^posts', views.get_posts),
    url(r'^authors', views.get_authors),
    url(r'^tags', views.get_tags),

    url(r'^filtered', views.get_filtered),
    url(r'^recommended', views.get_recommended),

    url(r'^home/$', RedirectView.as_view(url='/home/about')),
    url(r'^home/about$', views.about),
    url(r'^home/account_settings$', views.account_settings),
    url(r'^home/account_preferences$', views.account_preferences),
    url(r'^home/account_avatar$', views.account_avatar),

    url(r'^chat/$', views.chat, name='chat'),
    url(r'^friends/$', views.chat_friends, name='chat'),

    url(r'^pocket/login$', views.pocket_login),
    url(r'^feedly/login$', views.feedly_login),
]

urlpatterns = format_suffix_patterns(urlpatterns)
