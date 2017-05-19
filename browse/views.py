from django.shortcuts import render

from common import commonviews

from authentication.login_decorator import login_required


@login_required
def browse(request):
    context = dict()

    context.update(commonviews.side_menu('Browse'))
    return render(request, 'browse.html', context)
