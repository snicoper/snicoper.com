from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin,
)
from django.db.models import Sum
from django.views.generic import TemplateView

from blog.models import Article, Tag

UserModel = get_user_model()


class IndexView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'stats/index.html'
    permission_required = 'stats.can_edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Tags
        context['total_tags'] = Tag.objects.count()
        context['tag_most_viewed'] = Tag.objects.order_by('-views')[0]
        # Articles
        context['total_articles'] = Article.objects.count()
        context['total_views'] = Article.objects.all().aggregate(Sum('views'))
        context['article_most_viewed'] = Article.objects.order_by('-views')[0]
        context['article_most_voted'] = Article.objects.get_most_article_rate(quantity=5)
        # Usuarios
        context['num_users'] = UserModel.objects.count()
        context['last_register'] = UserModel.objects.last()
        return context
