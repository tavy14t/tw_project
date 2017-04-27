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
        'tag1': ['1', '2', '3'],
        'tag2': ['1', '3', '2', '4']
    }

    tag_data = collections.OrderedDict()

    for key in keys:
        tag_data[key] = []
        for item in keys[key]:
            data = {
                'info': item
            }

            tag_data[key].append(data)

    tag_table = collections.OrderedDict()

    for key in tag_data:
        uid = hex(random.randint(-10000, 10000))[2:]

        tag_table[key] = {
            'id': uid,
            'table': TagsTable(tag_data[key])
        }

    context['tags'] = tag_table

    return render(request, 'tags/tags.html', context)
