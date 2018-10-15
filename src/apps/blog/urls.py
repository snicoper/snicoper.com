from django.conf.urls import include, url

from . import views
from .api import urls as api_urls
from .feeds import LastedEntriesFeed

app_name = 'blog'

urlpatterns = [

    # Pagina principal del Blog, muestra todos los artículos.
    url(
        regex=r'^$',
        view=views.ArticleListView.as_view(),
        name='index'
    ),

    # Muestra un articulo.
    url(
        regex=r'^article/(?P<slug>[\w-]+)/$',
        view=views.ArticleDetailView.as_view(),
        name='article_detail'
    ),

    # Muestra la lista de etiquetas.
    url(
        regex=r'^tags/$',
        view=views.TagListView.as_view(),
        name='tag_list'
    ),

    # Muestra artículos por etiqueta.
    url(
        regex=r'^tag/(?P<slug>[\w-]+)/$',
        view=views.ArticleListByTagNameListView.as_view(),
        name='articles_by_tag'
    ),

    # Pagina principal de archives.
    url(
        regex=r'^archive/$',
        view=views.ArticleArchiveIndexView.as_view(),
        name='archive'
    ),

    # Archivo de artículos por año.
    url(
        regex=r'^archive/(?P<year>[\d]{4})/$',
        view=views.ArticleYearArchiveView.as_view(),
        name='archive_year'
    ),

    # Archivo de artículos por año/mes.
    url(
        regex=r'^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        view=views.ArticleMonthArchiveView.as_view(month_format='%m'),
        name='archive_month'
    ),

    # Formulario para recomendar articulo.
    url(
        regex=r'^recommend/(?P<slug>[-\w]+)/$',
        view=views.ArticleRecommendView.as_view(),
        name='article_recommend'
    ),

    # Registro para recibir notificaciones de nuevos artículos.
    url(
        regex=r'^alerts/register/$',
        view=views.ArticleSubscribeRegisterView.as_view(),
        name='article_suscriber_register'
    ),

    # DesRegistro para recibir notificaciones de nuevos artículos.
    url(
        regex=r'^alerts/unregister/(?P<token_unsigned>[\w]{30})/$',
        view=views.ArticleSubscribeUnregisterView.as_view(),
        name='article_suscriber_unregister'
    ),

    # Feeds del blog.
    url(
        regex=r'^feed/$',
        view=LastedEntriesFeed(),
        name='feed'
    ),

    # Api views.
    url(r'^api/', include(api_urls)),
]
