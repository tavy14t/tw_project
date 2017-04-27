from django.shortcuts import render

from common import commonviews

from authentication.login_decorator import custom_login_required


@custom_login_required
def browse(request):
    context = dict()

    context.update(commonviews.side_menu('Browse'))
    return render(request, 'browse/browse.html', context)
