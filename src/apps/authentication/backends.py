from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from . import settings as auth_settings

UserModel = get_user_model()


class EmailOrUsernameModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        """Backend para autenticación.

        Dependiendo de AUTH_TYPE comprobara que el tipo de autenticación del usuario:
            both: Email y username.
            username: username.
            email: email.

        Returns:
            User: El User en caso de éxito, None en caso contrario.
        """
        auth_type = auth_settings.AUTH_TYPE.lower()
        if auth_type == 'username':
            return super().authenticate(request, username, password, **kwargs)
        try:
            if auth_type == 'both':
                user = UserModel.objects.get(
                    Q(username__exact=username) | Q(email__exact=username)
                )
            else:
                user = UserModel.objects.get(email__exact=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
