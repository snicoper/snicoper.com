from django.conf import settings
from django.shortcuts import Http404, redirect


class AnonymousRequiredMixin(object):
    """Mixin para autorizar solo a usuarios anónimos."""

    def dispatch(self, request, *args, **kwargs):
        """Comprueba que sea un usuario anónimo.

        Si no es un usuario anónimo, lo redirecciona a la
        pagina LOGIN_REDIRECT_URL.
        """
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


class SuperuserRequiredMixin(object):
    """Solo un superuser puede visitar la pagina."""

    def dispatch(self, request, *args, **kwargs):
        """Si el usuario no esta logueado también lanza Http404."""
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class OwnerOrSuperuserRequiredMixin(object):
    """Solo el owner y superuser puede ver la view.

    Requiere un usuario autenticado.

    Requiere de un campo 'owner_field', que sera el campo a comprobar.
    Por defecto owner_field = 'owner'.
    """
    owner_field = 'owner'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        obj_owner = getattr(obj, self.owner_field)
        if not obj_owner:
            raise NotImplementedError('El campo {} no existe'.format(self.owner_field))
        user = request.user
        if not user.is_authenticated or obj_owner != user and not user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)
