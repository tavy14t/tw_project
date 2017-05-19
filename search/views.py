from django.shortcuts import render
from django.db import connection

from forms import SearchForm
from common import commonviews
from tables import InfoTable

import collections

from authentication.login_decorator import login_required


@login_required
def search(request):
    context = dict()

    context.update(commonviews.side_menu('Search'))

    search_form = SearchForm()

    if request.method == 'POST':
        search_form = SearchForm(request.POST)

        if search_form.is_valid() is False:
            print '[debug][search] Invalid search form text input!'

        else:
            name = search_form.cleaned_data['string']

            tabs = []
            context['title'] = 'Search'

            with connection.cursor() as cursor:
                cursor.execute("select * from users where firstname like '%{0}%'"
                               .format(name))

                aux = [(data[1], data[2]) for data in cursor]

                for firstname, lastname in aux:
                    tabs.append({
                        'info': firstname,
                        'value': lastname
                    })

            news = InfoTable(tabs, show_header=False)

            tabs = [('Users', {'data': news,
                                        'sidebar': False}),
                    ('Titles', {'data': news,
                                  'sidebar': False}), ]

            tabs = collections.OrderedDict(tabs)

            context['tabs'] = tabs

    context['form'] = search_form

    return render(request, 'search/search.html', context)
