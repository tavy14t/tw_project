from django.http import HttpResponseRedirect


def login_required(f):
    def wrap(request, *args, **kwargs):
        if 'userid' not in request.session.keys():
            return HttpResponseRedirect('/login')
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
