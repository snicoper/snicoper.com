from django.conf.urls import url

from . import views

# /blog/api/*
urlpatterns = [

    # Obtener votos de un articulo concreto.
    url(
        regex=r'^article/vote/details/(?P<pk>\d+)/$',
        view=views.ArticleRateDetailsAPIView.as_view(),
        name='upi_article_vote_details'
    ),

    # Vota positivo un articulo.
    url(
        regex=r'^article/vote/positive/(?P<pk>\d+)/$',
        view=views.ArticleRatePositiveUpdateAPIView.as_view(),
        name='upi_article_vote_positive'
    ),
]
