from django.contrib.sites.models import Site
from django.db.models import F
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.views.generic import TemplateView

from .models import AboutViews


class PageMixin(object):
    """Mixin para pages.

    Variables de clase:
    * template_name: Template .html (requerido)
    * template_md: Template .md (no requerido)
    * context_md: Contexto para templates *.md

    Requiere una URLConf para cada vista.

    Si no tiene valor template_md, simplemente renderiza
    la pagina .html.

    get_context_md similar a get_context_data pero para template_md.
    """
    template_md = None
    context_md = {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.template_md:
            try:
                context['template_md'] = get_template(self.template_md).render(
                    self.get_context_md()
                )
            except TemplateDoesNotExist:
                raise TemplateDoesNotExist('Template {} no existe'.format(self.template_md))
        return context

    def get_context_md(self):
        """Similar a get_context_data pero para el *.md."""
        return self.context_md


class CookieConsentView(PageMixin, TemplateView):
    """Muestra la política de cookies."""
    template_name = 'pages/cookie_consent.html'
    template_md = 'pages/cookie_consent.md'

    def get_context_md(self):
        context = super().get_context_md()
        context['site'] = Site.objects.get_current()
        return context


class AboutView(PageMixin, TemplateView):
    """Pagina de About.

    Cuanta el numero de visitas que tiene.
    """
    template_name = 'pages/about.html'
    model = AboutViews

    def dispatch(self, request, *args, **kwargs):
        if AboutViews.objects.count() == 0:
            AboutViews.objects.create()
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            AboutViews.objects.update(views=F('views') + 1)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['views_about'] = AboutViews.objects.get(pk=1)
        return context
