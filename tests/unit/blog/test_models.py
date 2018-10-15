import os

from django.core import mail
from django.core.files.images import get_image_dimensions
from django.utils.text import slugify

from blog.models import ArticleSubscribe, Tag
from tests.unit import images

from .base_blog import BaseBlogTest

image_path = os.path.join(os.path.dirname(__file__), 'image_test.jpg')


class TagTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.tag_data = {
            'title': 'Test Tag 3',
            'thumbnail': images.simple_uploaded_file(image_path)
        }
        self.tag = self.tag_model.objects.create(**self.tag_data)

    def tearDown(self):
        super().tearDown()
        if os.path.exists(self.tag.thumbnail.path):
            os.remove(self.tag.thumbnail.path)

    def test_fixtures(self):
        """Comprobar que los fixtures se han cargado."""
        self.assertGreater(self.tag_model.objects.count(), 1)
        self.assertGreater(self.article_model.objects.count(), 1)

    def test_str(self):
        """Devuelve el titulo."""
        self.assertEqual(str(self.tag), self.tag_data['title'])

    def test_admin_thumbnail(self):
        """Prueba el valor devuelto."""
        self.assertEqual(
            self.tag.admin_thumbnail(),
            '<img src="{}" alt="Tag thumbnail" width="100">'.format(self.tag.thumbnail.url)
        )

    def test_create_tag(self):
        """Crea una etiqueta."""
        self.assertGreater(Tag.objects.count(), 1)

    def test_slug_generado(self):
        """Comprueba que el slug ha sido generado."""
        self.assertTrue(self.tag.slug)
        self.assertEqual(self.tag.slug, slugify(self.tag.title))

    def test_field_thumbnail_required(self):
        """Si se intenta crear un modelo Tag sin el thumbnail, lanzara Exception."""
        with self.assertRaises(ValueError):
            Tag.objects.create(title='new test')

    def test_comprueba_numero_articulos_en_tag(self):
        """Comprueba el numero de artículos que pertenecen a una tag."""
        self.assertEqual(self.tag.get_num_articles_in_tag(), 0)
        article = self.article_model()
        article.owner = self.user
        article.default_tag = self.tag
        article.title = 'New Article'
        article.save()
        article.tags.add(self.tag)

        self.assertEqual(self.tag.get_num_articles_in_tag(), 1)

    def test_thumbnail_creado_width_400(self):
        """La imagen subida es redimensionada a un máximo de 400 de ancho."""
        width, height = get_image_dimensions(self.tag.thumbnail)

        self.assertEqual(width, 400)
        self.assertEqual(height, 250)

    def test_elimina_imagen_del_disco_cuando_se_elimina_tag(self):
        """Comprueba que elimina del disco el thumbnail."""
        image_path = self.tag.thumbnail.path
        self.tag.delete()

        self.assertFalse(os.path.exists(image_path))


class ArticleTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.tags = self.tag_model.objects.all()
        self.article_data = {
            "owner": self.user,
            "default_tag": self.tags[0],
            "title": "Test Article 100",
            "image_header": images.simple_uploaded_file(image_path),
            "body": "Test Article"
        }
        article = self.article_model.objects.create(**self.article_data)
        for tag in self.tags:
            article.tags.add(tag)
        article.save()
        self.article = article

    def tearDown(self):
        super().tearDown()
        if self.article.image_header and os.path.exists(self.article.image_header.path):
            os.remove(self.article.image_header.path)

    def test_creado_el_articulo(self):
        """Comprueba que se ha creado el articulo."""
        self.assertGreater(self.article_model.objects.count(), 1)

    def test_creado_slug(self):
        """Comprueba que se ha creado el slug."""
        self.assertEqual(self.article.slug, slugify(self.article.title))

    def test_str(self):
        """Devuelve el titulo."""
        self.assertEqual(str(self.article), self.article_data['title'])

    def test_get_str_tag_list(self):
        """Obtiene los tags en str separados por comas."""
        all_tags = ', '.join([tag.title for tag in self.tags])
        self.assertEqual(self.article.get_str_tag_list(), all_tags)

    def test_image_header(self):
        """Al cambiar una imagen, la antigua se elimina."""
        old_image_path = self.article.image_header.path

        self.assertTrue(os.path.exists(old_image_path))
        self.article.image_header = images.simple_uploaded_file(image_path)
        self.article.save()
        article = self.article_model.objects.get(pk=self.article.pk)
        new_image_path = article.image_header.path

        self.assertNotEqual(new_image_path, old_image_path)
        self.assertFalse(os.path.exists(old_image_path))
        self.assertTrue(os.path.exists(new_image_path))

        # Eliminar la nueva imagen si existe.
        if os.path.exists(new_image_path):
            os.remove(new_image_path)

    def test_image_header_limpiar(self):
        """Si desde la administración del articulo se pulsa
        limpiar en image_header, la imagen sera eliminada del disco.
        """
        image_path = self.article.image_header.path

        self.assertTrue(os.path.exists(image_path))
        self.article.image_header = None
        self.article.save()

        self.assertFalse(os.path.exists(image_path))

    def test_active_por_defecto_true(self):
        """Por defecto active es true."""
        self.assertTrue(self.article.active)

    def test_absolute_url(self):
        """Comprueba get_absolute_url, usa el slug para generar la url."""
        url = '/blog/article/{}/'.format(self.article.slug)
        self.assertEqual(self.article.get_absolute_url(), url)

    def test_send_article_subscribers(self):
        """Comprueba que envía un email a los usuarios suscritos al crear
        un articulo.
        """
        ArticleSubscribe.objects.create(email='snicoper@example.com')
        article_data = {
            "owner": self.user,
            "default_tag": self.tags[0],
            "title": "Test Article 1001",
            "body": "Test Article"
        }
        self.article_model.objects.create(**article_data)

        self.assertEqual(len(mail.outbox), 3)


class ArticleSubscribeTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.suscribe = ArticleSubscribe.objects.create(email='snicoper@example.com')

    def test_str(self):
        """Devuelve el email."""
        self.assertEqual(str(self.suscribe), self.suscribe.email)

    def test_subscriber_guardado_en_db(self):
        """Comprueba que se ha guardado en la db."""
        self.assertGreater(ArticleSubscribe.objects.count(), 1)

    def test_se_ha_generado_token(self):
        """Comprueba que el token se ha generado."""
        self.assertTrue(self.suscribe.token_unsigned)

    def test_length_token(self):
        """El token generado es de 30 caracteres."""
        self.assertEqual(len(self.suscribe.token_unsigned), 30)
