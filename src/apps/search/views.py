from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet


class ArticleSearchView(SearchView):
    template_name = 'search/search_article.html'
    queryset = SearchQuerySet().order_by('-create_at')
    paginate_by = 10
