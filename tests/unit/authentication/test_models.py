from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils.crypto import get_random_string

from authentication.models import UserEmailUpdate
from tests.unit.authentication.base_auth import BaseAuthTest

UserModel = get_user_model()


class RegisterUserTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.model_data = {
            'username': 'palote',
            'email': 'palote@example.com',
            'password': 'UnPasswordTes123'
        }

    def register_user(self):
        """Obtener una instancia de RegisterUser."""
        return self.register_model.objects.create(**self.model_data)

    def test_registro_valido(self):
        """Crea un registro valido."""
        register = self.register_user()
        self.assertEqual(self.register_model.objects.count(), 1)

        # Se ha creado el token
        self.assertTrue(register.token)
        self.assertEqual(len(register.token), 32)

        # El make_password lo genera el form.
        self.assertEqual(register.password, self.model_data['password'])

        # date_joined
        self.assertTrue(register.date_joined)

    def test_str(self):
        """Obtiene el email."""
        register = self.register_user()
        self.assertEqual(str(register), register.email)

    def test_generate_token_genera_32_caracteres(self):
        """El método 'privado' _generate_token."""
        self.register_user()
        token = self.register_model()._generate_token()

        self.assertEqual(len(token), 32)

    def test_username_unico(self):
        """Comprueba los campos únicos."""
        self.model_data['email'] = 'user@example.com'
        self.register_user()

        # username ya esta en uso.
        with self.assertRaises(IntegrityError):
            self.register_user()

    def test_email_unico(self):
        """Comprueba los campos únicos."""
        self.model_data['username'] = 'userexamplecom'
        self.register_user()

        # username ya esta en uso.
        with self.assertRaises(IntegrityError):
            self.register_user()

    def test_min_length_username(self):
        """Mínimo caracteres para el username."""
        self.model_data['username'] = 'per'
        register = self.register_model()

        with self.assertRaises(ValidationError):
            register.full_clean()

    def test_username_validators(self):
        """Mínimo caracteres para el username."""
        self.model_data['username'] = '-pericopalote'
        self.model_data['token'] = get_random_string(length=32)
        register = self.register_model(**self.model_data)

        with self.assertRaises(ValidationError):
            register.full_clean()

        self.model_data['username'] = 'peri copalote'
        self.model_data['token'] = get_random_string(length=32)
        register = self.register_model(**self.model_data)

        with self.assertRaises(ValidationError):
            register.full_clean()

        self.model_data['username'] = 'peri-copalote'
        self.model_data['token'] = get_random_string(length=32)
        register = self.register_model(**self.model_data)

        with self.assertRaises(ValidationError):
            register.full_clean()

        self.model_data['username'] = 'pericopalote'
        self.model_data['token'] = get_random_string(length=32)
        register = self.register_model(**self.model_data)

        # Si no lanza ValidationError, todo OK
        register.full_clean()


class UserEmailUpdateTest(BaseAuthTest):

    def setUp(self):
        super().setUp()
        self.username = 'testuser'
        self.password = '123'
        self.email = 'usertest@example.com'
        self.user = UserModel.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )

    def test_simple_create(self):
        """Comprueba que un token ha de tener 30 caracteres."""
        email_update = UserEmailUpdate.objects.create(
            user=self.user,
            new_email='emailtest@example.com',
            token=get_random_string(length=30)
        )

        self.assertEqual(UserEmailUpdate.objects.count(), 1)
        self.assertEqual(len(email_update.token), 30)

    def test_str(self):
        """Obtiene el nombre de usuario."""
        UserEmailUpdate.objects.create(
            user=self.user,
            new_email='emailtest@example.com',
            token=get_random_string(length=30)
        )
        self.assertEqual(str(self.user.user_email_update), self.username)
