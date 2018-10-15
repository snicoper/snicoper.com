from django.core import mail
from django.urls import reverse
from django.utils import timezone

from blog.models import Article, ArticleSubscribe

from .base_blog import BaseBlogTest


class ArticleListViewTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('blog:index'))
        self.tags = self.tag_model.objects.all()

    def test_status_code_200_user_anonimo(self):
        """Devuelve status_code 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba que usa el template 'blog/article_list.html'"""
        self.assertTemplateUsed(self.response, 'blog/article_list.html')

    def test_comprueba_context_items_mostrados(self):
        """Comprueba que muestra los items creados."""
        self.assertGreater(len(self.response.context['article_list']), 1)

    def test_no_mostrar_mas_de_12_items_por_pagina(self):
        """Mostrara 12 items por pagina.

        Comprueba también que en la pagina 2 hay al menos 2 item.
        TODO: Se crean mas fixtures, revisar esta parte.
        """
        for i in range(10, 22):
            self.article_model.objects.create(
                owner=self.user,
                default_tag=self.tags[0],
                title='Test Article {}'.format(i)
            )

        self.assertGreater(Article.objects.count(), 12)

        response = self.client.get(reverse('blog:index'))
        self.assertEqual(len(response.context['article_list']), 12)

        response = self.client.get('{}?page=2'.format(reverse('blog:index')))
        self.assertGreater(len(response.context['article_list']), 1)


class ArticleDetailViewTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.article = self.article_model.objects.get(pk=1)
        self.url_reverse = reverse('blog:article_detail', kwargs={'slug': self.article.slug})
        self.tags = self.tag_model.objects.all()
        self.response = self.client.get(self.url_reverse)

    def test_status_code_200_user_anonimo(self):
        """Devuelve status_code 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba que usa el template 'blog/article_detail.html'"""
        self.assertTemplateUsed(self.response, 'blog/article_detail.html')

    def test_incrementa_en_1_en_detalles_del_articulo(self):
        """Al ver detalles del articulo, incrementa en 1."""
        old_views = self.article_model.objects.get(pk=1).views
        self.client.get(reverse('blog:article_detail', kwargs={'slug': self.article.slug}))
        new_views = self.article_model.objects.get(pk=1).views

        self.assertEqual(old_views + 1, new_views)

    def test_variables_context_existen(self):
        """Comprueba algunas variables del contexto."""
        self.assertTrue(self.response.context['article'])
        self.assertTrue(self.response.context['article'].title)
        self.assertTrue(self.response.context['article'].body)


class TagListViewTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('blog:tag_list'))

    def test_status_code_200_user_anonimo(self):
        """Devuelve status_code 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_template_usado(self):
        """Comprueba que usa el template 'blog/tag_list.html'"""
        self.assertTemplateUsed(self.response, 'blog/tag_list.html')

    def test_variables_context_existen(self):
        """Comprueba algunas variables del contexto."""
        self.assertTrue(self.response.context['tag_list'])
        self.assertGreater(len(self.response.context['tag_list']), 1)


class ArticleRecommendViewTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        article = self.article_model.objects.get(pk=1)
        self.url = reverse('blog:article_recommend', kwargs={'slug': article.slug})
        self.response = self.client.get(self.url)
        self.form_data = {
            'name': 'test_user',
            'from_email': 'from_email@example.com',
            'to_email': 'to_email@example.com',
            'message': 'message'
        }

    def test_article_recommended_status_code_200(self):
        """blog:article_recommended retorna status_code 200."""
        self.assertTrue(self.response.status_code, 200)

    def test_template_cargado(self):
        """Comprueba el template cargado."""
        self.assertTemplateUsed(self.response, 'blog/article_recommend.html')

    def test_form_valid_redirect_to_article_detail(self):
        """Un formulario valido, redireccionara otra vez al articulo."""
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 302)

    def test_form_invalid_vuelve_a_mostrar_el_formulario(self):
        """Si el formulario no es valido, lo vuelve a mostrar."""
        self.form_data['name'] = ''
        response = self.client.post(self.url, data=self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recomendar articulo')

    def test_envia_email(self):
        """Comprueba que el email ha sido enviado."""
        self.client.post(self.url, data=self.form_data)

        self.assertEqual(len(mail.outbox), 1)


class ArticleArchiveViewTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.tags = self.tag_model.objects.all()
        self.article = self.article_model.objects.get(pk=1)
        for i in range(10, 14):
            self.article_model.objects.create(
                owner=self.user,
                default_tag=self.tags[0],
                title='Test Article {}'.format(i)
            )
        self.year = self.article.create_at.year
        self.response = self.client.get(reverse('blog:archive'))

    def test_archive_status_code_200(self):
        """blog:archive devuelve status_code 200."""
        status_code = self.client.get(reverse('blog:archive')).status_code
        self.assertEqual(status_code, 200)

    def test_archive_template_usado(self):
        """Comprueba blog:archive el template usado."""
        self.assertTemplateUsed(self.response, 'blog/article_archive_index.html')

    def test_muestra_el_actual_year_en_el_template(self):
        """Muestra el año actual en el template."""
        self.assertContains(self.response, self.year)


class ArticleYearArchiveViewTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.tags = self.tag_model.objects.all()
        for i in range(10, 14):
            self.article_model.objects.create(
                owner=self.user,
                default_tag=self.tags[0],
                title='Test Article {}'.format(i)
            )
        self.response = self.client.get(reverse(
            'blog:archive_year', kwargs={'year': timezone.now().year})
        )

    def test_archive_year_status_code_200(self):
        """Comprueba que archive_year status_code es 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_archive_year_template_usado(self):
        """Comprueba el template usado por blog:archive_year."""
        self.assertTemplateUsed(self.response, 'blog/article_archive_year.html')


class ArticleMonthArchiveViewTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.tags = self.tag_model.objects.all()
        self.use = self.user_model.objects.get(pk=1)
        for i in range(10, 14):
            self.article_model.objects.create(
                owner=self.user,
                default_tag=self.tags[0],
                title='Test Article {}'.format(i)
            )
        self.response = self.client.get(
            reverse('blog:archive_month', kwargs={
                'year': timezone.now().year,
                'month': timezone.now().month
            })
        )

    def test_archive_month_status_code_200(self):
        """Comprueba que archive_month status_code es 200."""
        self.assertEqual(self.response.status_code, 200)

    def test_archive_year_template_usado(self):
        """Comprueba el template usado por blog:archive_month."""
        self.assertTemplateUsed(self.response, 'blog/article_archive_month.html')


class LastedEntriesFeedTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.tags = self.tag_model.objects.all()
        self.use = self.user_model.objects.get(pk=1)
        for i in range(10, 14):
            self.article_model.objects.create(
                owner=self.user,
                default_tag=self.tags[0],
                title='Test Article {}'.format(i)
            )
        self.response = self.client.get(reverse('blog:feed'))

    def test_feed_status_code_200(self):
        """blog:fedd obtiene un status_code 200."""
        self.assertEqual(self.response.status_code, 200)


class SitemapsTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.tags = self.tag_model.objects.all()
        self.use = self.user_model.objects.get(pk=1)
        for i in range(10, 14):
            self.article_model.objects.create(
                owner=self.user,
                default_tag=self.tags[0],
                title='Test Article {}'.format(i)
            )

    def test_sitemap_status_code_200(self):
        """Comprueba el status code de /sitemap.xml"""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)


class ArticleSubscribeRegisterViewTest(BaseBlogTest):

    def setUp(self):
        super().setUp()
        self.tags = self.tag_model.objects.all()
        self.use = self.user_model.objects.get(pk=1)

    def test_registra_email_correctamente(self):
        """Registra un email valido correctamente."""
        self._register_email(1)

        self.assertEqual(ArticleSubscribe.objects.count(), 2)

    def test_envia_email_cuando_se_crea_un_articulo(self):
        """Enviá un email a todos los usuarios registrados."""
        self._register_email(10)

        # Comprueba que se han registrado los emails.
        self.assertGreater(ArticleSubscribe.objects.count(), 1)

        self.article_model.objects.create(
            owner=self.user,
            default_tag=self.tags[0],
            title='New Article 36',
            body='Article body'
        )

        self.assertGreater(len(mail.outbox), 1)

    def _register_email(self, num):
        for i in range(0, num):
            email = 'testuser{}@example.com'.format(i)
            form_data = {'user_email': email}
            self.client.post(
                reverse('blog:article_suscriber_register'),
                data=form_data
            )


class ArticleSubscribeUnregisterViewTest(BaseBlogTest):

    def test_elimina_una_alerta(self):
        """Elimina una alerta de artículos correctamente."""
        form_data = {'user_email': 'testuser@example.com'}
        self.client.post(
            reverse('blog:article_suscriber_register'),
            data=form_data
        )
        alert = ArticleSubscribe.objects.first()
        url = reverse(
            'blog:article_suscriber_unregister',
            kwargs={'token_unsigned': alert.token_unsigned}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ArticleSubscribe.objects.count(), 1)
