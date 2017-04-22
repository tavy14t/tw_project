from models import Users


class AuthenticationBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if password in user._meta.get_field('passworhash'):
                return user
        return None