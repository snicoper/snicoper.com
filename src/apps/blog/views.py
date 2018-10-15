from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db.models import Count, F
from django.shortcuts import Http404, get_object_or_404, redirect
from django.template.loader import get_template
from django.views import generic

from .forms import ArticleRecommendForm
from .models import Article, ArticleSubscribe, Tag


class ArticleListView(generic.ListView):
    """Muestra lista de artículos."""
    template_name = 'blog/article_list.html'
    context_object_name = 'article_list'
    model = Article
    paginate_by = 12

    def get_queryset(self):
        if self.queryset is not None:
            queryset = self.queryset.published()
        else:
            queryset = self.model.objects.published()
        return queryset.select_related(
            'owner',
            'default_tag',
            'article_rate'
        ).prefetch_related('tags')


class ArticleDetailView(generic.DetailView):
    """Detalles del articulo."""
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'
    model = Article

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            self.model.objects.filter(slug=kwargs.get('slug')).update(views=F('views') + 1)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().select_related('owner')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_most_view_list'] = Article.objects.published().order_by('-views')[:10]
        context['article_most_vote_list'] = Article.objects.get_most_article_rate()
        return context


class TagListView(generic.ListView):
    """Muestra lista de etiquetas."""
    template_name = 'blog/tag_list.html'
    context_object_name = 'tag_list'
    model = Tag

    def get_queryset(self):
        """Añade la propiedad articles_count, con la cantidad de
        artículos en cada Tag.
        """
        return super().get_queryset().annotate(
            articles_count=Count('article_tags')
        )


class ArticleListByTagNameListView(ArticleListView):
    """Muestra artículos de una categoría."""

    def dispatch(self, request, *args, **kwargs):
        """Incrementa +1 'Tag.views'."""
        slug = self.kwargs.get('slug')
        get_object_or_404(Tag, slug=slug)
        self.model.objects.filter(slug=slug).update(views=F('views') + 1)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Obtener lista de artículos por tag categoría."""
        return super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))


class ArticleRecommendView(generic.FormView):
    """Recomienda un articulo por email a una persona."""
    form_class = ArticleRecommendForm
    template_name = 'blog/article_recommend.html'

    def get_context_data(self, **kwargs):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        context = super().get_context_data(**kwargs)
        context['article'] = article
        return context

    def get_form(self, form_class=None):
        """Inicializar campos name y from_email si es un usuario logueado."""
        form = super().get_form(form_class)
        user = self.request.user
        if user.is_authenticated:
            form['from_email'].initial = user.email
            if user.get_full_name():
                form['name'].initial = user.get_full_name()
        return form

    def form_valid(self, form):
        article = get_object_or_404(Article, slug=self.kwargs.get('slug'))
        messages.success(self.request, 'Se ha enviado el mensaje correctamente.')
        cdata = form.cleaned_data
        context = {
            'article': article,
            'name': cdata['name'],
            'message': cdata['message'],
            'site': get_current_site(self.request),
            'protocol': 'https://' if self.request.is_secure() else 'http://'
        }
        template_email = get_template('blog/emails/article_recommend.txt').render(context)
        send_mail(
            subject='{} te recomienda que leas un articulo'.format(cdata['name']),
            message=template_email,
            from_email=cdata['from_email'],
            recipient_list=[cdata['to_email']]
        )
        return redirect(article.get_absolute_url())


class ArticleArchiveIndexView(generic.TemplateView):
    """Mostrar por años y meses numero de artículos."""
    template_name = 'blog/article_archive_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {'archive': self._archive_articles()}
        return context

    def _archive_articles(self):
        """Obtiene artículos y los ordena por año."""
        articles = Article.objects.published()
        archive = {}
        date_field = 'create_at'
        years = articles.datetimes(date_field, 'year')[::-1]
        for year in years:
            months = articles.filter(create_at__year=year.year).\
                datetimes(date_field, 'month')
            archive[year] = months
        archive = sorted(archive.items(), reverse=True)
        return archive


class ArticleArchiveMixin(object):
    queryset = Article.objects.published()
    allow_future = False
    make_object_list = True
    date_field = 'create_at'


class ArticleYearArchiveView(ArticleArchiveMixin, generic.YearArchiveView):
    """Mostrar el archivo de artículos por año."""
    template_name = 'blog/article_archive_year.html'


class ArticleMonthArchiveView(ArticleArchiveMixin, generic.MonthArchiveView):
    """Mostrar el archivo de artículos por mes."""
    template_name = 'blog/article_archive_month.html'


class ArticleSubscribeRegisterView(generic.View):
    """Suscribe un email para nuevos artículos."""

    def get(self, request, *args, **kwargs):
        raise Http404

    def post(self, request, *args, **kwargs):
        url_redirect = request.GET.get('next', '/')
        email = request.POST.get('user_email', None)
        try:
            validate_email(email)
            if ArticleSubscribe.objects.filter(email=email):
                messages.error(request, 'Email ya registrado')
            else:
                ArticleSubscribe.objects.create(email=email)
                messages.success(request, 'Email registrado correctamente')
        except ValidationError:
            messages.error(request, 'Email no valido')
        return redirect(url_redirect)


class ArticleSubscribeUnregisterView(generic.View):
    """Unsubscribe un email para nuevos artículos."""

    def get(self, request, *args, **kwargs):
        token_unsigned = kwargs.get('token_unsigned', None)
        if token_unsigned:
            subscribers = ArticleSubscribe.objects.filter(token_unsigned=token_unsigned)
            if subscribers.exists():
                email = subscribers[0].email
                subscribers[0].delete()
                messages.success(request, 'Email {} eliminado!'.format(email))
        return redirect('/')
