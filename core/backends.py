from django.contrib.auth.backends import ModelBackend as BaseModelBackend
from SGU.models import Usuario


class ModelBackend(BaseModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username is None:
            try:
                user = Usuario.objects.get(email=username)
                if user.check_password(password):
                    return user
            except Usuario.DoesNotExist:
                pass
