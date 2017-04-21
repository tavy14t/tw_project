from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connection

from forms import SearchForm
from common import commonviews
from tables import InfoTable
from home.models import Users

import collections


@login_required(login_url='/')
def search(request):
    context = dict()

    context.update(commonviews.side_menu('Search'))

    search_form = SearchForm()

    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid() is False:
            print 'Invalid Input'

        else:
            name = search_form.cleaned_data['string']

            tabs = []
            context['title'] = 'Search'

            with connection.cursor() as cursor:
                cursor.execute("select * from users where firstname like '%{0}%'"
                               .format(name))

                context['data'] = [data[1] for data in cursor]
                for data in context['data']:
                    tabs.append({
                        'info': 'nume1',
                        'value': data
                    })

            news = InfoTable(tabs, show_header=False)

            tabs = [('Identification', {'data': news,
                                        'sidebar': False}),
                    ('Salutare', {'data': news,
                                  'sidebar': False}), ]

            tabs = collections.OrderedDict(tabs)

            context['tabs'] = tabs

    context['form'] = search_form

    return render(request, 'search/search.html', context)
