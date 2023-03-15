from django.contrib.auth import get_user_model


class UsernameAuthBackend(object):
    '''
    Authenticate using a username.
    '''
    User = get_user_model()

    def authenticate(self, request, username=None, password=None):
        try:
            user = self.User.objects.get(username=username)
            if user.check_password(password):
                return user
            return None
        except self.User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.User.objects.get(pk=user_id)
        except self.User.DoesNotExist:
            return None
