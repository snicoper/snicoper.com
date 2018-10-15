from haystack import indexes

from blog.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    """Búsquedas en blog.Article."""
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    body = indexes.CharField(model_attr='body')
    create_at = indexes.DateTimeField(model_attr='create_at')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.published()
