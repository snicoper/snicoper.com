from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.views.static import serve

from blog.sitemaps import BlogSitemap
from blog.views import ArticleListView

sitemaps = {
    'blog': BlogSitemap
}

# i18n_patterns
urlpatterns = [

    ##################################################
    # / Pagina de inicio.
    url(r'^$', ArticleListView.as_view(), name='home_page'),
    ##################################################

    # /accounts/*
    url(r'^accounts/', include('accounts.urls')),

    # /auth/*
    url(r'^auth/', include('authentication.urls')),

    # /blog/*
    url(r'^blog/', include('blog.urls')),

    # /contact/*
    url(r'^contact/', include('contact.urls')),

    # /home/*
    url(r'^home/', include('home.urls')),

    # /pages/*
    url(r'^pages/', include('pages.urls')),

    # /search/*
    url(r'^search/', include('search.urls')),

    # /stats/*
    url(r'^stats/', include('stats.urls')),

    # /sitemap.xml
    url(
        regex=r'^sitemap\.xml$',
        view=sitemap,
        kwargs={'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),

    # /admin/*
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    import debug_toolbar

    urlpatterns += [
        # /media/:<mixed>path/
        url(
            regex=r'^media/(?P<path>.*)$',
            view=serve,
            kwargs={'document_root': settings.MEDIA_ROOT}
        ),

        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
