from django.contrib.auth.hashers import make_password
from django.urls import reverse

from authentication import settings as auth_settings

from .base_auth import BaseAuthTest


class EmailOrUsernameModelBackend(BaseAuthTest):

    def __init__(self, *args, **kwargs):
        self._default_auth_type = auth_settings.AUTH_TYPE
        super().__init__(*args, **kwargs)

    def setUp(self):
        super().setUp()
        self.url = reverse('authentication:login')
        self.logout()

    def tearDown(self):
        """Asegurarse de que AUTH_TYPE queda con los valores por defecto."""
        super().tearDown()
        setattr(auth_settings, 'AUTH_TYPE', self._default_auth_type)

    def test_auth_type_default_username(self):
        """Prueba authenticate con AUTH_TYPE por defecto."""
        form_data = {
            'username': self.user.username,
            'password': '123'
        }
        response = self.client.post(self.url, data=form_data)
        expected_url = reverse('accounts:profile')

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_auth_type_default_email(self):
        """No permite login con email, es el default."""
        form_data = {
            'username': self.user.email,
            'password': '123'
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

        # El usuario no esta logueado.
        user = response.context['user']
        self.assertTrue(user.is_anonymous)

    def test_auth_type_both(self):
        """Con AUTH_TYPE='both'."""
        setattr(auth_settings, 'AUTH_TYPE', 'both')

        # Email.
        form_data = {
            'username': self.user.email,
            'password': '123'
        }
        response = self.client.post(self.url, data=form_data)
        expected_url = reverse('accounts:profile')

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        self.client.logout()

        # Username.
        form_data = {
            'username': self.user.email,
            'password': '123'
        }
        response = self.client.post(self.url, data=form_data)
        expected_url = reverse('accounts:profile')

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

    def test_auth_type_email(self):
        """Con AUTH_TYPE='email', username fallara."""
        setattr(auth_settings, 'AUTH_TYPE', 'email')

        # Email.
        form_data = {
            'username': self.user.email,
            'password': '123'
        }
        response = self.client.post(self.url, data=form_data)
        expected_url = reverse('accounts:profile')

        self.assertRedirects(
            response=response,
            expected_url=expected_url,
            status_code=302,
            target_status_code=200
        )

        self.client.logout()

        # Username fallara.
        form_data = {
            'username': self.user.username,
            'password': '123'
        }
        response = self.client.post(self.url, data=form_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

        # El usuario no esta logueado.
        user = response.context['user']
        self.assertTrue(user.is_anonymous)

    def test_case_sensitive_en_username_y_password(self):
        """Nombre de usuario, email y password es case sensitive."""
        setattr(auth_settings, 'AUTH_TYPE', 'both')
        # Cambiar el password del usuario.
        raw_passord = 'aBcDe123'
        self.user.password = make_password(raw_passord)
        self.user.save()

        # Username en mayúsculas no logueara.
        form_data = {
            'username': self.user.username.upper(),
            'password': raw_passord
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        user = response.context['user']
        self.assertTrue(user.is_anonymous)

        # Email en mayúsculas no logueara.
        form_data = {
            'username': self.user.email.upper(),
            'password': raw_passord
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        user = response.context['user']
        self.assertTrue(user.is_anonymous)

        # Password en mayúsculas no logueara.
        form_data = {
            'username': self.user.email,
            'password': raw_passord.upper()
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        user = response.context['user']
        self.assertTrue(user.is_anonymous)
