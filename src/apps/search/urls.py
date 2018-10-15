from django.conf.urls import url

from . import views

app_name = 'search'

urlpatterns = [

    # Búsqueda en los artículos
    url(
        regex=r'^$',
        view=views.ArticleSearchView.as_view(),
        name='articles'
    ),
]
