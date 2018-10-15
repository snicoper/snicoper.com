from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Article


class BlogSitemap(Sitemap):
    changefreq = 'never'
    protocol = 'https'
    priority = 0.5

    def items(self):
        return Article.objects.published()

    def lastmod(self, obj):
        return obj.create_at

    def location(self, item):
        return reverse(item)
