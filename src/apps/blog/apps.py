from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    varbose_name = 'Blog Application'

    def ready(self):
        from . import signals
