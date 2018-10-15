from django.contrib.auth.hashers import make_password
from django.contrib.sites.models import Site
from django.core import mail
from django.urls import reverse
from django.utils import timezone

from config.settings import local as settings_local
from tests.unit.authentication.base_auth import BaseAuthTest


class RegisterUserFormViewTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'authentication:register'
        self.url = reverse(self.urlconf)

    def test_status_code(self):
        """Prueba status_code para usuarios."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # Usuario logueado lo redirige a profile.
        self.login()
        expected_url = reverse('accounts:profile')
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Prueba el template_name."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'authentication/register.html')

    def test_delete_expired_registers(self):
        """El método __init__ es el que elimina los registros caducados."""
        register = self.register_model.objects.create(
            username='palote',
            password=make_password('123DSDSF'),
            email='palote@example.com',
            date_joined=timezone.now() - timezone.timedelta(
                days=self.auth_settings.AUTH_REGISTER_EXPIRE_DAYS,
                hours=5
            )
        )

        # Verifica que es menor a now()
        self.assertTrue(register.date_joined < timezone.now())

        # Accediendo a la vista, en __init__ ejecutara
        # authentication.utils.delete_expired_registers y elimina
        # los registros < a AUTH_REGISTER_EXPIRE_DAYS
        self.client.get(self.url)

        self.assertEqual(self.register_model.objects.count(), 0)

    def test_nuevo_registro(self):
        """Crea un registro y verifica que se ha creado en la db, que se ha
        enviado un email y el get_success_url.
        """
        form_data = {
            'username': 'newtestuser',
            'email': 'newtestuser@example.com',
            'password': 'MiPasswordTestUser123',
            'password2': 'MiPasswordTestUser123'
        }
        response = self.client.post(self.url, data=form_data, follow=True)

        # Form OK y redirecciona.
        self.assertRedirects(
            response=response,
            expected_url=reverse('authentication:success'),
            status_code=302,
            target_status_code=200
        )

        # get_success_url
        self.assertTemplateUsed(response, 'authentication/success.html')

        # Recibido Email.
        current_site = Site.objects.get(pk=1)
        self.assertEqual(len(mail.outbox), 1)

        subject = 'Validación de email en {}'.format(current_site.name)
        self.assertEqual(mail.outbox[0].subject, subject)


class RegisterUserSuccessViewTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'authentication:success'
        self.url = reverse(self.urlconf)

    def test_status_code(self):
        """Prueba status_code para usuarios."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # Usuario logueado lo redirige a profile.
        self.login()
        expected_url = reverse('accounts:profile')
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Prueba el template_name."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'authentication/success.html')


class RegisterUserValidateTokenViewTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.model_data = {
            'username': 'newtestuser',
            'email': 'newtestuser@example.com',
            'password': 'MiPasswordTestUser123'
        }
        self.token = self.register_model.objects.create(**self.model_data).token
        self.urlconf = 'authentication:validate_token'
        self.url = reverse(self.urlconf, kwargs={'token': self.token})

    def test_status_code(self):
        """Prueba status_code para usuarios."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # Usuario logueado lo redirige a profile.
        self.login()
        expected_url = reverse('accounts:profile')
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Prueba el template_name."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'authentication/validate_token.html')

    def test_el_usuario_se_a_movido_a_accounts_user(self):
        """Si todo OK, el usuario se elimina de RegisterUser y
        lo crea en accounts.models.User.
        """
        self.assertEqual(self.register_model.objects.count(), 1)
        self.client.get(self.url)
        self.assertEqual(self.register_model.objects.count(), 0)
        new_user = self.user_model.objects.get(username=self.model_data['username'])
        self.assertTrue(new_user)


class LoginViewTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'authentication:login'
        self.url = reverse(self.urlconf)

    def test_status_code(self):
        """Prueba status_code para usuarios."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        # Usuario logueado lo redirige a profile.
        self.login()
        expected_url = reverse('accounts:profile')
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_template_usado(self):
        """Prueba el template_name."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'authentication/login.html')


class LogoutView(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'authentication:logout'
        self.url = reverse(self.urlconf)

    def test_status_code(self):
        """Prueba status_code para usuarios."""
        self.login()
        response = self.client.get(self.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/article_list.html')


class PasswordResetViewTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'authentication:password_reset'
        self.url = reverse(self.urlconf)

    def test_status_code(self):
        """Prueba status_code para usuarios."""
        response = self.client.get(self.url, follow=True)

        self.assertTemplateUsed(response, 'authentication/password_reset_form.html')


class UserEmailUpdateViewTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'authentication:email_update'
        self.url = reverse(self.urlconf)
        self.login()

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 404)

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'authentication/email_update.html')

    def test_initials(self):
        """Comprueba los campos con initial."""
        response = self.client.get(self.url)
        form = response.context['form'].initial

        # Usuario
        self.assertEqual(form['user'], self.user.id)

        # Existe un token, el token es random.
        self.assertTrue(form['token'])

        # El token es de 30 caracteres.
        self.assertEqual(len(form['token']), 30)

        # Email actual del usuario, se establece en al campo new_email.
        self.assertEqual(form['new_email'], self.user.email)

    def test_email_en_uso(self):
        """No puede poner un Email en uso."""
        perico = self.user_model.objects.get(pk=2)
        response = self.client.get(self.url)
        form = response.context['form'].initial
        form['new_email'] = perico.email
        form['re_new_email'] = perico.email
        response = self.client.post(self.url, data=form)
        form = response.context['form']

        self.assertFalse(form.is_valid())

    def test_cambia_el_email(self):
        """Cambia el Email y sera notificado por Email."""
        response = self.client.get(self.url)
        form = response.context['form'].initial
        form['new_email'] = 'new_email@example.com'
        form['re_new_email'] = 'new_email@example.com'
        response = self.client.post(self.url, data=form, follow=True)

        # Comprueba la redirección.
        self.assertRedirects(
            response=response,
            expected_url=reverse('accounts:profile'),
            status_code=302,
            target_status_code=200
        )

        # Los cambios aun no se han realizado.
        user = self.user_model.objects.get(pk=1)

        self.assertEqual(self.user.email, user.email)

        # Comprueba que ha recibido un Email.
        self.assertEqual(len(mail.outbox), 1)

    def test_email_enviado(self):
        """Prueba del Email enviado."""
        response = self.client.get(self.url)
        form = response.context['form'].initial
        form['new_email'] = 'new_email@example.com'
        form['re_new_email'] = 'new_email@example.com'
        self.client.post(self.url, data=form)
        outbox = mail.outbox[0]

        # Titulo del Email.
        self.assertEqual(outbox.subject, 'Confirmación cambio de email')

        # From.
        self.assertEqual(outbox.from_email, settings_local.GROUP_EMAILS['NO-REPLY'])


class UserEmailUpdateValidateViewTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.login()

        # Es necesario generar un token
        response = self.client.get(reverse('authentication:email_update'))
        form = response.context['form'].initial
        self.token = form['token']
        form['new_email'] = 'new_email@example.com'
        form['re_new_email'] = 'new_email@example.com'
        self.client.post(reverse('authentication:email_update'), data=form)

        self.urlconf = 'authentication:email_update_validate'
        self.url = reverse(self.urlconf, kwargs={'token': self.token})

    def test_usuario_anonimo_redirecciona(self):
        """Un usuario anónimo lo redirecciona a settings.LOGIN_URL."""
        self.client.logout()
        response = self.client.get(self.url)

        self.assertTrue(response.status_code, 404)

    def test_redirect_success(self):
        """Si es código es valido, redirecciona a accounts:profile."""
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(
            response=response,
            expected_url=reverse('accounts:profile'),
            status_code=302,
            target_status_code=200
        )

    def test_redirect_no_success(self):
        """Si es codigo no es valido, redirecciona a authentication:token_not_exists."""
        token = self.token[:-4] + '1234'
        rev = reverse(self.urlconf, kwargs={'token': token})
        response = self.client.get(rev)

        self.assertRedirects(
            response=response,
            expected_url=reverse('authentication:token_email_not_exists'),
            status_code=302,
            target_status_code=200
        )


class UserEmailUpdateNotFoundViewTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.urlconf = 'authentication:token_email_not_exists'
        self.url = reverse(self.urlconf)

    def test_status_code_200(self):
        """El status_code es 200 cuando esta logueado."""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_template_usado(self):
        """Comprueba el template usado."""
        response = self.client.get(self.url)

        self.assertTemplateUsed(response, 'authentication/token_email_not_exists.html')
