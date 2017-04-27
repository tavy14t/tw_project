from django.shortcuts import render

from common import commonviews
from tables import TagsTable

import random
import collections

from authentication.login_decorator import custom_login_required


@custom_login_required
def tags(request):
    context = dict()

    context.update(commonviews.side_menu('Tags'))

    keys = {
        'tag1': ['', 'abc', 'asb'],
        'tag2': ['zas', 'zdf', 'zvd', 'zza']
    }

    context['tags'] = [key for key in keys]

    if request.method == 'POST':
        tags = request.POST.getlist('values')
        tag_data = collections.OrderedDict()

        tag_data = []
        for key in tags:
            for item in keys[key]:
                tag_data.append({
                    'info': item
                })

        tag_table = collections.OrderedDict()

        uid = hex(random.randint(-10000, 10000))[2:]

        tag_table = {
            'id': uid,
            'table': TagsTable(tag_data)
        }

        context['prefered_tags'] = tag_table

    return render(request, 'tags/tags.html', context)
