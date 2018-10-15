from django import forms
from django.contrib.auth.forms import (
    UserChangeForm as AuthUserChangeForm,
    UserCreationForm as AuthUserCreationForm,
)

from .models import User


class UserChangeForm(AuthUserChangeForm):
    """Form para editar usuario en admin."""

    class Meta(AuthUserChangeForm.Meta):
        model = User


class UserCreationForm(AuthUserCreationForm):
    """Form creación de usuarios."""

    class Meta(AuthUserCreationForm.Meta):
        model = User


class UserProfileUpdateForm(forms.ModelForm):
    """Editar perfil de usuario por el propio usuario.

    La diferencia de UserChangeForm son los fields.
    """

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone')


class UserUpdateAvatarForm(forms.ModelForm):
    """Form para añadir/cambiar el avatar del usuario."""
    delete_avatar = forms.BooleanField(
        label='Eliminar mi avatar',
        required=False
    )

    class Meta:
        model = User
        fields = ('avatar',)
