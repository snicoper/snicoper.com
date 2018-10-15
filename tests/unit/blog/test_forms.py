from django.test import TestCase

from blog.forms import ArticleRecommendForm


class ArticleRecommendFormTest(TestCase):

    def setUp(self):
        super().setUp()
        self.form_data = {
            'name': 'test_user',
            'from_email': 'formemail@example.com',
            'to_email': 'toemail@example.com',
            'message': 'Test message'
        }

    def test_form_is_valid(self):
        """Comprueba que el formulario es valido."""
        form = ArticleRecommendForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_todos_los_campos_son_obligatorios(self):
        """Comprueba que todos los campos son obligatorios."""
        tmp = self.form_data['name']
        self.form_data['name'] = ''
        form = ArticleRecommendForm(data=self.form_data)

        self.assertFalse(form.is_valid())

        self.form_data['name'] = tmp
        tmp = self.form_data['from_email']
        self.form_data['from_email'] = ''
        form = ArticleRecommendForm(data=self.form_data)

        self.assertFalse(form.is_valid())

        self.form_data['from_email'] = tmp
        self.form_data['to_email'] = ''
        form = ArticleRecommendForm(data=self.form_data)

        self.assertFalse(form.is_valid())

    def test_message_no_es_necesario(self):
        """El campo message no es obligatorio."""
        self.form_data['message'] = ''
        form = ArticleRecommendForm(data=self.form_data)
        self.assertTrue(form.is_valid())
