from django.conf import settings
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _

from .settings import AUTH_MIN_LENGTH_USERNAME, AUTH_REGEX_USERNAME


class RegisterUser(models.Model):
    """Registro de un usuario.

    Lo registra como usuario temporal, luego ha de validar el token.

    Los registros expirados los elimina la view RegisterUserFormView.
    """
    username = models.CharField(
        verbose_name=_('Nombre de usuario'),
        max_length=150,
        unique=True,
        validators=[
            MinLengthValidator(AUTH_MIN_LENGTH_USERNAME),
            RegexValidator(AUTH_REGEX_USERNAME)
        ]
    )
    email = models.EmailField(
        verbose_name=_('Email'),
        unique=True
    )
    password = models.CharField(
        verbose_name=_('Contraseña'),
        max_length=128
    )
    token = models.CharField(
        verbose_name=_('Token'),
        max_length=32
    )
    date_joined = models.DateTimeField(
        verbose_name=_('Fecha de registro'),
        default=timezone.now
    )

    class Meta:
        verbose_name = _('Registro usuario temporal')
        verbose_name_plural = _('Registro usuarios temporales')

    def __str__(self):
        return self.email

    def save(self, **kwargs):
        if not self.id:
            self.token = self._generate_token()
        return super().save(**kwargs)

    def _generate_token(self):
        while True:
            token = get_random_string(length=32)
            if not RegisterUser.objects.filter(token=token):
                return token


class UserEmailUpdate(models.Model):
    """Guarda un token para su posterior verificación."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='user_email_update',
        verbose_name=_('Usuario')
    )
    new_email = models.EmailField(
        verbose_name=_('Nuevo email')
    )
    token = models.CharField(
        verbose_name=_('Token'),
        max_length=30
    )
    create_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('Actualizar email')
        verbose_name_plural = _('Actualizar emails')

    def __str__(self):
        return self.user.username
