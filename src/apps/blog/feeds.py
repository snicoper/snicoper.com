from django.contrib.syndication.views import Feed

import markdown2

from .models import Article


class LastedEntriesFeed(Feed):
    """Feed de las entradas del Blog."""
    title = 'Blog de Salvador Nicolas'
    link = '/blog/'
    description = 'Blog personal de Salvador Nicolas sobre Linux y programación Web.'

    def items(self):
        return Article.objects.order_by('-id')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return markdown2.markdown(item.body)

    def item_link(self, item):
        return item.get_absolute_url()
