from django.db import models
from django.db.models import F


class ArticleManager(models.Manager):

    def published(self, **kwargs):
        """Solo los artículos que estén actives."""
        return self.get_queryset().filter(active=True, **kwargs)

    def get_most_article_rate(self, quantity=10):
        """Obtener un numero de articulo ordenados por votos de ArticleRatio."""
        article_list = self.published().\
            prefetch_related('article_rate').\
            order_by('-article_rate__positives')[:quantity]
        return article_list


class ArticleRateManager(models.Manager):

    def add_positive_article(self, request, article_id):
        """Vota un articulo con un positivo.

        Returns:
            True en caso de establecer el voto, False en caso contrario.
        """
        try:
            super().get_queryset().filter(
                article__pk=article_id
            ).update(positives=F('positives') + 1)
            return True
        except:
            pass
        return False
