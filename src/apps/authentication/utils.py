from django.utils import timezone

from . import settings as auth_settings
from .models import RegisterUser


def delete_expired_registers():
    """Elimina registros expirados.

    Elimina los registros no finalizados y expirado de RegisterUser.
    """
    days = auth_settings.AUTH_REGISTER_EXPIRE_DAYS
    diff = timezone.now() - timezone.timedelta(days=days)
    RegisterUser.objects.filter(date_joined__lt=diff).delete()
