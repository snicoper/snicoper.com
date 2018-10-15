from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from utils.images import ImageResize
from utils.mixins.models import ImageUpdateModel

from . import settings as accounts_settings


class User(ImageUpdateModel, AbstractUser):
    """Model para usuarios."""
    avatar = models.ImageField(
        verbose_name='Avatar',
        upload_to=accounts_settings.ACCOUNTS_AVATAR_PATH,
        default='',
        blank=True
    )
    phone = models.CharField(
        verbose_name='Teléfono',
        max_length=25,
        default='',
        blank=True
    )

    _image_fields = ['avatar']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_avatar = self.avatar

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        """Comprueba si ha añadido o cambiado el avatar y lo re-dimensiona"""
        if self.avatar and self.old_avatar != self.avatar:
            super().save(*args, **kwargs)
            image_resize = ImageResize(self.avatar.path)
            image_resize.resize(
                save_path=self.avatar.path,
                width=accounts_settings.ACCOUNTS_AVATAR_WIDTH,
                height=accounts_settings.ACCOUNTS_AVATAR_HEIGHT
            )
            self.old_avatar = self.avatar
        else:
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('accounts:profile')

    @property
    def get_avatar(self):
        """Obtener avatar usuario.

        Al usar get_avatar no requiere de {{ MEDIA_URL }}.

        Returns:
            str: Avatar del usuario o imagen por defecto.

            Si el usuario tiene un avatar, obtendrá el del usuario, en caso
            contrario, el avatar por defecto.
        """
        if not self.avatar or not self.avatar.path:
            return '{}{}/{}'.format(
                settings.MEDIA_URL,
                accounts_settings.ACCOUNTS_AVATAR_PATH,
                accounts_settings.ACCOUNTS_AVATAR_DEFAULT
            )
        return '{}/{}'.format(settings.MEDIA_URL, self.avatar)
