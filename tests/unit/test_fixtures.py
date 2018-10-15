from django.contrib.sites.models import Site

from .base_test import BaseTestCase


class FixturesTest(BaseTestCase):
    """Comprueba que los fixtures se han creado."""

    def test_users(self):
        """Numero de usuarios."""
        # Numero de usuarios.
        users = self.user_model.objects.all()
        self.assertEqual(users.count(), 2)

        # Usuario snicoper
        user = self.user_model.objects.get(pk=1)
        self.assertEqual(user.username, 'snicoper')
        self.assertEqual(user.email, 'snicoper@snicoper.com')
        self.assertTrue(self.client.login(username='snicoper', password='123'))
        self.assertEqual(user.first_name, 'Salvador')
        self.assertEqual(user.last_name, 'Nicolas')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_sites(self):
        """Sites se ha restaurado."""
        site = Site.objects.get(pk=1)

        self.assertEqual(site.name, 'snicoper.com')
        self.assertEqual(site.domain, '127.0.0.1:8000')
