from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext as _
from django.views import generic

from utils.http import get_full_path
from utils.mail import send_templated_mail
from utils.mixins.views import AnonymousRequiredMixin

from .forms import AuthenticationForm, RegisterUserForm, UserEmailUpdateForm
from .models import RegisterUser, UserEmailUpdate
from .utils import delete_expired_registers

UserModel = get_user_model()


class RegisterUserFormView(AnonymousRequiredMixin, generic.CreateView):
    """Muestra el formulario de registro."""
    template_name = 'authentication/register.html'
    form_class = RegisterUserForm
    model = RegisterUser

    def __init__(self, *args, **kwargs):
        """Elimina posibles usuarios expirados."""
        delete_expired_registers()
        super().__init__(*args, **kwargs)

    def get_success_url(self):
        """Si todo OK, envía el email para verificación y direcciona."""
        self._send_email_with_token()
        return reverse('authentication:success')

    def _send_email_with_token(self):
        """Envía un email con token para terminar proceso de registro."""
        current_site = get_current_site(self.request)
        site_name = current_site.name
        url_validate_token = get_full_path(
            self.request,
            'authentication:validate_token',
            token=self.object.token
        )
        context = {
            'username': self.object.username,
            'email': self.object.email,
            'site_name': site_name,
            'url_validate_token': url_validate_token
        }
        send_templated_mail(
            subject=_('Validación de email en {}').format(site_name),
            from_email=settings.GROUP_EMAILS['NO-REPLY'],
            recipients=[self.object.email],
            context=context,
            template_text='authentication/emails/register_success.txt'
        )


class RegisterUserSuccessView(AnonymousRequiredMixin, generic.TemplateView):
    template_name = 'authentication/success.html'


class RegisterUserValidateTokenView(AnonymousRequiredMixin, generic.TemplateView):
    """Validación email de un nuevo registro a través del token."""
    template_name = 'authentication/validate_token.html'

    def get(self, request, *args, **kwargs):
        delete_expired_registers()
        token = self.kwargs.get('token')
        try:
            user_temp = RegisterUser.objects.get(token=token)
        except RegisterUser.DoesNotExist:
            return render(request, 'authentication/token_not_exists.html')
        self._move_user_temp_to_user(user_temp)
        return super().get(request, *args, **kwargs)

    def _move_user_temp_to_user(self, user_temp):
        """Mueve usuario temporal a auth_user y elimina el temporal."""
        user_model = UserModel.objects.create(
            username=user_temp.username,
            email=user_temp.email,
            password=user_temp.password
        )
        if user_model:
            user_temp.delete()


class LoginView(AnonymousRequiredMixin, views.LoginView):
    template_name = 'authentication/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        msg = 'Bienvenido de nuevo {}'.format(self.request.user.username)
        messages.success(self.request, msg)
        return super().get_success_url()


class LogoutView(LoginRequiredMixin, views.LogoutView):
    template_name = 'authentication/logged_out.html'
    next_page = reverse_lazy('home_page')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Gracias por el tiempo que ha dedicado hoy al sitio web.')
        return super().dispatch(request, *args, **kwargs)


class PasswordResetView(AnonymousRequiredMixin, views.PasswordResetView):
    template_name = 'authentication/password_reset_form.html'
    email_template_name = 'authentication/emails/password_reset_email.html'
    subject_template_name = 'authentication/emails/password_reset_subject.txt'
    success_url = reverse_lazy('authentication:password_reset_done')


class PasswordResetDoneView(AnonymousRequiredMixin, views.PasswordResetDoneView):
    template_name = 'authentication/password_reset_done.html'


class PasswordResetConfirmView(AnonymousRequiredMixin, views.PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('authentication:password_reset_complete')


class PasswordResetCompleteView(AnonymousRequiredMixin, views.PasswordResetCompleteView):
    template_name = 'authentication/password_reset_complete.html'


class PasswordChangeView(views.PasswordChangeView):
    template_name = 'authentication/password_change_form.html'
    success_url = reverse_lazy('authentication:password_change_done')


class PasswordChangeDoneView(views.PasswordChangeDoneView):
    template_name = 'authentication/password_change_done.html'


class UserEmailUpdateView(LoginRequiredMixin, generic.FormView):
    """Muestra el formulario para cambiar el email."""
    template_name = 'authentication/email_update.html'
    form_class = UserEmailUpdateForm
    model = UserEmailUpdate

    def get_initial(self):
        """Establece datos en los campos del form."""
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['token'] = self._generate_unique_token()
        initial['new_email'] = self.request.user.email
        return initial

    def form_valid(self, form):
        """Enviá el email de confirmación."""
        new_email = form.cleaned_data['new_email']
        token = form.cleaned_data['token']
        self._update_or_create_model(token, new_email)
        self._send_confirm_email_for_validate(token, new_email)
        return super().form_valid(form)

    def get_success_url(self):
        msg = _('Se ha enviado un email a la nueva dirección para la confirmación')
        messages.success(self.request, msg)
        return reverse('accounts:profile')

    def _generate_unique_token(self):
        """Genera un token único.

        Comprueba que no exista uno igual en la db.

        Returns:
            str: Token generado de 30 caracteres.
        """
        while True:
            token = get_random_string(length=30)
            if not UserEmailUpdate.objects.filter(token=token):
                return token

    def _update_or_create_model(self, token, new_email):
        """Crear o actualiza un nuevo email en UserEmailUpdate."""
        UserEmailUpdate.objects.update_or_create(
            defaults={'new_email': new_email, 'token': token},
            user=self.request.user
        )

    def _send_confirm_email_for_validate(self, token, new_email):
        """Enviá un email para la confirmación del nuevo email con un token."""
        current_site = get_current_site(self.request)
        url_validate_token = get_full_path(
            self.request,
            'authentication:email_update_validate',
            token=token
        )
        context = {
            'url_validate_token': url_validate_token,
            'site_name': current_site.name
        }
        send_templated_mail(
            subject=_('Confirmación cambio de email'),
            from_email=settings.GROUP_EMAILS['NO-REPLY'],
            recipients=[new_email],
            context=context,
            template_text='authentication/emails/email_update_confirm.txt'
        )


class UserEmailUpdateValidateView(LoginRequiredMixin, generic.View):
    """Verifica el token de cambio de email.

    Para mayor seguridad, el usuario ha de estar logueado.

    Una vez comprobado y actualizado el nuevo email, elimina el
    email temporal.
    """

    def get(self, request, *args, **kwargs):
        """Comprueba el token que coincida."""
        token = kwargs.get('token')
        try:
            email_update = UserEmailUpdate.objects.get(token=token, user=request.user)
        except UserEmailUpdate.DoesNotExist:
            return redirect('authentication:token_email_not_exists')
        self.request.user.email = email_update.new_email
        self.request.user.save()
        email_update.delete()
        messages.success(request, _('Se ha actualizado el email'))
        return redirect(reverse('accounts:profile'))


class UserEmailUpdateNotFoundView(generic.TemplateView):
    """El token no existe o no pertenece al usuario."""
    template_name = 'authentication/token_email_not_exists.html'
