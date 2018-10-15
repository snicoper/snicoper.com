from django.conf import settings
from django.contrib.sitemaps import ping_google
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string

from utils.mail import send_templated_mail
from utils.mixins.models import ImageUpdateModel, SlugFieldModel

from .managers import ArticleManager, ArticleRateManager


class Tag(SlugFieldModel, ImageUpdateModel, models.Model):
    """Etiquetas de los artículos"""
    _image_fields = ['thumbnail']

    views = models.IntegerField(
        verbose_name='Vistas',
        default=0
    )
    thumbnail = models.ImageField(
        verbose_name='Miniatura',
        upload_to='articles/tags'
    )

    class Meta:
        ordering = ('-views',)
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'

    def get_num_articles_in_tag(self):
        """Obtener el numero de artículos de la etiqueta."""
        return self.article_tags.count()

    get_num_articles_in_tag.short_description = 'Num. artículos'

    def admin_thumbnail(self):
        return '<img src="{}" alt="Tag thumbnail" width="100">'.format(self.thumbnail.url)

    admin_thumbnail.short_description = 'Miniatura'
    admin_thumbnail.allow_tags = True


class Article(SlugFieldModel, ImageUpdateModel, models.Model):
    """Artículos del blog."""
    _image_fields = ['image_header']

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='article_owner',
        verbose_name='Autor'
    )
    tags = models.ManyToManyField(
        to=Tag,
        related_name='article_tags',
        verbose_name='Etiquetas'
    )
    default_tag = models.ForeignKey(
        to=Tag,
        on_delete=models.CASCADE,
        related_name='article_default_tag',
        verbose_name='Etiqueta principal'
    )
    image_header = models.ImageField(
        verbose_name='Imagen cabecera',
        upload_to='articles/headers',
        blank=True,
        null=True
    )
    body = models.TextField(
        verbose_name='Cuerpo'
    )
    active = models.BooleanField(
        verbose_name='Activo',
        default=True
    )
    views = models.IntegerField(
        verbose_name='Vistas',
        default=0
    )
    create_at = models.DateTimeField(
        verbose_name='Fecha creación',
        auto_now_add=True
    )
    update_at = models.DateTimeField(
        verbose_name='Fecha modificación',
        auto_now=True
    )

    objects = ArticleManager()

    class Meta:
        ordering = ('-create_at',)
        verbose_name = 'Articulo'
        verbose_name_plural = 'artículos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Antes de guardar, comprobar si se esta creando el Article.
        created = not self.id
        super().save(*args, **kwargs)
        if created and settings.DEBUG is False:
            # Enviar notificación del articulo a los subscritos.
            self._send_article_suscribers()
            try:
                ping_google()
            except Exception:
                pass
        if created:
            # Crea ArticleRate para las votaciones por cada articulo creado.
            ArticleRate.objects.create(article=self)

    def get_absolute_url(self):
        return reverse('blog:article_detail', kwargs={'slug': self.slug})

    def get_str_tag_list(self):
        return ', '.join([t.title for t in self.tags.all()])

    get_str_tag_list.short_description = 'Etiquetas'

    def _send_article_suscribers(self):
        """Enviá un email a todos los que estén suscritos."""
        site = Site.objects.get_current()
        site_domain = site.domain
        link_article = '{}{}'.format(site_domain, self.get_absolute_url())
        subject = 'Nuevo articulo en {}'.format(site_domain),
        template_text = 'blog/emails/article_suscribed.txt'
        from_email = settings.DEFAULT_FROM_EMAIL
        for signed in list(ArticleSubscribe.objects.all()):
            link_unsigned = '{}{}'.format(
                site_domain,
                reverse(
                    'blog:article_suscriber_unregister',
                    kwargs={'token_unsigned': signed.token_unsigned}
                )
            )
            context = {
                'site_domain': site_domain,
                'link_article': link_article,
                'link_unsigned': link_unsigned
            }
            send_templated_mail(
                subject=subject,
                from_email=from_email,
                recipients=[signed.email],
                context=context,
                template_text=template_text
            )


class ArticleSubscribe(models.Model):
    """Suscripción para recibir alertas de nuevos artículos por email."""
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )
    token_unsigned = models.CharField(
        verbose_name='Token unregister',
        max_length=30,
        unique=True
    )

    class Meta:
        verbose_name = 'Subscrito a artículos'
        verbose_name_plural = 'Subscritos a artículos'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.id:
            while True:
                self.token_unsigned = get_random_string(length=30)
                if not ArticleSubscribe.objects.filter(token_unsigned=self.token_unsigned):
                    break
        return super().save(*args, **kwargs)


class ArticleRate(models.Model):
    """Ratio de un articulo."""
    article = models.OneToOneField(
        to=Article,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='article_rate',
        verbose_name='Ratio articulo',
    )
    positives = models.PositiveIntegerField(default=0)

    objects = ArticleRateManager()

    def __str__(self):
        return self.article.title
