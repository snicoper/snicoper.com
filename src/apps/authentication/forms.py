from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm as AuthForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext, ugettext_lazy as _

from . import settings as auth_settings
from .models import RegisterUser

UserModel = get_user_model()


class AuthenticationForm(AuthForm):
    """Formulario de login."""

    def __init__(self, *args, **kwargs):
        """Cambiar el label de 'username' según AUTH_TYPE."""
        auth_type = auth_settings.AUTH_TYPE.lower()
        super().__init__(*args, **kwargs)
        if auth_type == 'email':
            self.fields['username'].label = ugettext('Tu email')
        if auth_type == 'both':
            self.fields['username'].label = ugettext('Nombre de usuario o email')


class RegisterUserForm(forms.ModelForm):
    """Formulario de registro."""

    password2 = forms.CharField(
        label=_('Confirme contraseña'),
        widget=forms.PasswordInput()
    )

    class Meta:
        model = RegisterUser
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }
        help_texts = {
            'username': _('Solo letras y números, ha de comenzar por una letra')
        }

    def clean_password(self):
        """Prueba que sea una contraseña segura.

        Usa settings.AUTH_PASSWORD_VALIDATORS para ver si la contraseña se
        ajusta.
        Si no se ajusta, validate_password lanzara un ValidationError.

        Returns:
            str: Si pasa la validación, el password hasheado.
        """
        password = self.cleaned_data['password']
        validate_password(password)
        return make_password(password)

    def clean_password2(self):
        """Prueba que password y password2 sean iguales.

        password se obtiene el raw data del form.
        """
        password = self.data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(ugettext('Los dos campos de contraseña no coinciden'))
        return password2

    def clean_username(self):
        """Prueba que no exista en la db accounts.User.

        Prueba que el nombre de usuario no sea uno en AUTH_USERNAME_BLACKLIS.

        RegisterUser al ser un campo unique, ya se encarga de no tener un
        username igual.
        """
        username = self.cleaned_data['username']
        if UserModel.objects.filter(username=username):
            raise forms.ValidationError(ugettext('El usuario ya existe'))
        if username.lower() in auth_settings.AUTH_USERNAME_BLACKLIST:
            raise forms.ValidationError('Nombre de usuario no valido')
        return username

    def clean_email(self):
        """Prueba que no exista en la db accounts.User.

        RegisterUser al ser un campo unique, ya se encarga de no tener un
        email igual.
        """
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email):
            raise forms.ValidationError(ugettext('El email ya existe'))
        return email


class UserEmailUpdateForm(forms.Form):
    """Cambia el email de un usuario."""
    new_email = forms.EmailField(
        label=_('Nuevo email')
    )
    re_new_email = forms.EmailField(
        label=_('Confirma el nuevo email')
    )
    token = forms.CharField(
        widget=forms.HiddenInput()
    )
    user = forms.CharField(
        widget=forms.HiddenInput()
    )

    def clean(self):
        """Validación de new_email y re_new_email.

        Comprueba que ambos sean iguales y que no este registrado ya en la db.
        """
        cleaned_data = super().clean()
        new_email = cleaned_data.get('new_email')
        re_new_email = cleaned_data.get('re_new_email')
        if new_email and new_email != re_new_email:
            raise forms.ValidationError(ugettext('Los emails no coinciden'))
        return cleaned_data

    def clean_new_email(self):
        """Comprueba que el email no exista en la db.

        También lo prueba en la tabla RegisterUser.
        """
        new_email = self.cleaned_data['new_email']
        if (UserModel.objects.filter(email=new_email) or
                RegisterUser.objects.filter(email=new_email)):
            raise forms.ValidationError(ugettext('El email ya existe'))
        return new_email
