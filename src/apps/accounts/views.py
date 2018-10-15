from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.views import generic

from .forms import UserProfileUpdateForm, UserUpdateAvatarForm
from .models import User


class UserProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/profile.html'


class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Actualiza perfil de usuario."""
    template_name = 'accounts/profile_update.html'
    form_class = UserProfileUpdateForm
    model = User

    def get_object(self, queryset=None):
        """Obtener usuario actual."""
        return self.request.user

    def get_success_url(self):
        msg_success = 'Se ha actualizado los datos del perfil'
        messages.success(self.request, msg_success)
        return super().get_success_url()


class UserAvatarUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Añadir/Actualizar avatar de usuario."""
    template_name = 'accounts/avatar_update.html'
    form_class = UserUpdateAvatarForm
    model = User

    def get_object(self, queryset=None):
        """Obtener usuario actual."""
        return self.request.user

    def get_context_data(self, **kwargs):
        """Si el usuario tiene un avatar, mostrara el campo para limpiarlo."""
        context = super().get_context_data(**kwargs)
        if self.request.user.avatar:
            context['has_avatar'] = True
        return context

    def form_valid(self, form):
        """Reset avatar si pulsa marca delete_avatar.

        Si el usuario ha pulsado en delete_avatar, el campo avatar
        se pondrá en '', por lo que restablecerá el valor por defecto.
        """
        if form.cleaned_data['delete_avatar']:
            instance = form.save(commit=False)
            instance.avatar = ''
        return super().form_valid(form)

    def get_success_url(self):
        msg_success = 'Se ha actualizado el avatar'
        messages.success(self.request, msg_success)
        return reverse('accounts:profile')
