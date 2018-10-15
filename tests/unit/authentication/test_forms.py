from django.utils.crypto import get_random_string

from authentication import forms
from authentication.models import RegisterUser
from tests.unit.authentication.base_auth import BaseAuthTest


class AuthenticationFormTest(BaseAuthTest):
    """Este form solo comprueba los campos.

    Los validators, etc, son los de Django y eso no se prueba.
    """

    def setUp(self):
        super().setUp()
        self.form_data = {
            'username': 'snicoper',
            'password': '123'
        }

    def get_form(self):
        """Obtener una instancia de AuthenticationForm."""
        return forms.AuthenticationForm(data=self.form_data)

    def test_form_valid(self):
        """Form valido."""
        form = self.get_form()

        self.assertTrue(form.is_valid())


class RegisterUserFormTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.form_data = {
            'username': 'testuser',
            'email': 'testuser123@example.com',
            'password': 'MiPasswordSecreto123',
            'password2': 'MiPasswordSecreto123',
        }

    def get_form(self):
        """Obtener una instancia de RegisterUserForm."""
        return forms.RegisterUserForm(data=self.form_data)

    def test_form_valid(self):
        """Prueba un form valido."""
        form = self.get_form()

        self.assertTrue(form.is_valid())

    def test_passwords_diferentes(self):
        """Prueba el form con passwords diferentes."""
        self.form_data['password2'] = '123456'
        form = self.get_form()

        self.assertFalse(form.is_valid())

    def test_password_validators(self):
        """Prueba los validators de password."""
        # Demasiado corta
        self.form_data['password'] = 'DfT'
        self.form_data['password2'] = 'DfT'
        form = self.get_form()

        self.assertFalse(form.is_valid())

        # Passwords numérico
        self.form_data['password'] = '123123123'
        self.form_data['password2'] = '123123123'
        form = self.get_form()

        self.assertFalse(form.is_valid())

        # Passwords numérico
        self.form_data['password'] = 'aslfdkj·"$"234'
        self.form_data['password2'] = 'aslfdkj·"$"234'
        form = self.get_form()

        self.assertTrue(form.is_valid())

    def test_username_existe(self):
        """Username existe en accounts.User.

        En models.RegisterUser ya prueba que no exista, por ser un campo unique
        y se prueba en test_models.py
        """
        self.form_data['username'] = self.user_model.objects.get(pk=1).username
        form = self.get_form()

        self.assertFalse(form.is_valid())

    def test_email_existe(self):
        """Username existe en accounts.User.

        En models.RegisterUser ya prueba que no exista, por ser un campo unique
        y se prueba en test_models.py
        """
        self.form_data['email'] = self.user_model.objects.get(pk=1).email
        form = self.get_form()

        self.assertFalse(form.is_valid())


class UserEmailUpdateFormTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.form = forms.UserEmailUpdateForm
        self.form_data = {
            'user': self.user,
            'new_email': 'test@example.com',
            're_new_email': 'test@example.com',
            'token': get_random_string(length=32)
        }

    def test_form_valid(self):
        """Prueba un form valido."""
        form = self.form(data=self.form_data)

        self.assertTrue(form.is_valid())

    def test_emails_han_de_ser_iguales(self):
        """Si new_email o re_new_email son diferentes, fallara."""
        self.form_data['re_new_email'] = 'different@example.com'

        form = self.form(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_email_ya_existe(self):
        """Prueba si existe el Email en la tabla usuarios o en RegisterUser."""
        RegisterUser.objects.create(
            username='testnewuser',
            email='test12@example.com',
            password='12333221',
            token=get_random_string(length=32)
        )
        self.form_data['new_email'] = 'test12@example.com'
        self.form_data['re_new_email'] = 'test12@example.com'
        form = self.form(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['new_email'][0],
            'El email ya existe'
        )
