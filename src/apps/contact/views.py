from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.core.mail import EmailMessage
from django.shortcuts import Http404, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.views import generic

from .forms import ContactForm
from .models import ContactMessage

UserModel = get_user_model()


class ContactView(generic.FormView):
    """Muestra un formulario de contacto.

    Si es un usuario anónimo, mostrara el campo email,
    si es un usuario logueado, no mostrara el campo email.
    """
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def __init__(self, **kwargs):
        """Crear propiedades."""
        self.subject = None
        self.message = None
        self.user_email = None
        self.is_register = False
        super().__init__(**kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields['email'].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        self.subject = form.cleaned_data['subject']
        self.message = form.cleaned_data['message']
        self.user_email = form.cleaned_data['email']
        self.is_register = self.request.user.is_authenticated
        self._send_email_notification()
        self._register_notification_in_db()
        msg_success = 'Se ha enviado el email a un administrador'
        messages.success(self.request, msg_success)
        return redirect(reverse('blog:index'))

    def _send_email_notification(self):
        context_email = {
            'register': 'registrado ' if self.is_register else 'no registrado ',
            'user_email': self.user_email,
            'subject': self.subject,
            'message': self.message
        }
        template_email = get_template('contact/emails/contact.txt').render(context_email)
        send_mail = EmailMessage(
            subject=self.subject,
            body=template_email,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[mail for mail in settings.GROUP_EMAILS['CONTACTS']],
            reply_to=[self.user_email]
        )
        send_mail.send()

    def _register_notification_in_db(self):
        """Registra en la db un mensaje de contacto."""
        ContactMessage.objects.create(
            subject=self.subject,
            message=self.message,
            email=self.user_email,
            is_register=self.is_register
        )


class BaseContactMessage(PermissionRequiredMixin, AccessMixin):
    """Requiere permisos para ver los mensajes o lanzara 404."""
    model = ContactMessage
    permission_required = 'contact.can_view_messages'

    def handle_no_permission(self):
        raise Http404


class ContactMessageListView(BaseContactMessage, generic.ListView):
    template_name = 'contact/message_list.html'
    context_object_name = 'message_list'
    paginate_by = 10


class ContactMessageDetailView(BaseContactMessage, generic.DetailView):
    template_name = 'contact/message_detail.html'
    context_object_name = 'message'

    def get_context_data(self, **kwargs):
        """Comprueba si es un usuario registrado.

        Si es un usuario registrado, obtener nombre de usuario.
        Si no lo esta, marcara el mensaje como leído.
        """
        context = super().get_context_data(**kwargs)
        message = self.get_object()
        if message.is_register:
            context['username'] = UserModel.objects.get(email=message.email).username
        if not message.read:
            message.read = True
            message.save()
        return context
