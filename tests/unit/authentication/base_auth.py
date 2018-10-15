from authentication import settings as auth_settings
from authentication.models import RegisterUser
from tests.unit.base_test import BaseTestCase


class BaseAuthTest(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.register_model = RegisterUser
        self.auth_settings = auth_settings
