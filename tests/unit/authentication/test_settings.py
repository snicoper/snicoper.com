from tests.unit.authentication.base_auth import BaseAuthTest


class SettingsTest(BaseAuthTest):

    def setUp(self):
        super().setUp()

    def test_settings(self):
        """Prueba los valores de settings."""

        self.assertEqual(self.auth_settings.AUTH_TYPE, 'username')
        self.assertEqual(self.auth_settings.AUTH_REGISTER_EXPIRE_DAYS, 3)
        self.assertEqual(
            self.auth_settings.AUTH_REGEX_USERNAME,
            r'^[a-zA-Z]{1}[a-zA-Z0-9]+$'
        )
        self.assertEqual(self.auth_settings.AUTH_MIN_LENGTH_USERNAME, 5)
