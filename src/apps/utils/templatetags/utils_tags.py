from django import template
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

import markdown2

register = template.Library()


@register.simple_tag(name='markdown')
def markdown_format(text, safe=False):
    """Devuelve el texto markdown en HTML.

    Example:
        Con un texto seguro.
        {% markdown resource.description safe=True %}
        {% markdown resource.description True %}

        Con un texto inseguro.
        {% markdown resource.description safe=False %}
        {% markdown resource.description False %}
        {% markdown resource.description %}

    Args:
        text (str): Texto markdown
        safe (bool): El texto es seguro? de lo contrario lo escapa.

    Returns:
        str: El markdown convertido en HTML.
    """
    if not safe:
        # Si no es safe, el texto siempre se escapa.
        text = escape(text)
    return mark_safe(
        markdown2.markdown(
            text,
            extras=['fenced-code-blocks']
        )
    )


@register.simple_tag(takes_context=True)
def is_active(context, urlconf_name, **kwargs):
    """Devolverá active si request.path coincide con urlconf_name.

    Comprueba con URLConf con request.path.

    Example:
        <li class="{% is_active 'blog:index' %}">

    Args:
        context: Contexto en el template.
        urlconf_name (str): URLConf
        kwargs (dict): parámetros de reverse('', kwargs=kwargs)

    Returns:
        (str): si coincide devolverá 'active' en caso contrario un string vacío ''.
    """
    url_reverse = reverse(urlconf_name, kwargs=kwargs)
    if context['request'].path == url_reverse:
        return 'active'
    return ''


@register.simple_tag(name='pagination')
def pagination(page_obj):
    initial = 1
    radius = 3
    pages = radius * 2 + 1
    num_pages = page_obj.paginator.num_pages
    last = pages if num_pages > pages else num_pages
    if page_obj.number > (radius + 1):
        initial = page_obj.number - radius
        if num_pages > page_obj.number + radius:
            last = page_obj.number + radius
        else:
            last = num_pages
    context = {
        'initial': initial,
        'last': last,
        'num_pages': num_pages,
        'current': page_obj.number,
        'range': range(initial, last + 1),
        'has_pagination': True if num_pages > 1 else False
    }
    return context


@register.simple_tag(name='next_pagination', takes_context=True)
def next_pagination(context):
    """La paginación se hace en función de si tiene un query en GET.

    Para paginación, pagina siguiente si existe.

    Example:
        <a href="{% next_pagination %}">next</a>

    Si en el query de una URI existe ?page=xx, cambiara solo la parte
    del ?page=xxx por el nuevo numero de pagina. En caso contrario,
    añadirá page=xxx al query string.
    """
    request = context['request']
    page_obj = context['page_obj']
    uri = request.GET.urlencode()
    if not uri:
        return '?page={}'.format(page_obj.next_page_number())
    if 'page' in uri:
        page = 'page={}'.format(page_obj.number)
        new_uri = uri.replace(page, 'page={}'.format(page_obj.next_page_number()))
        return '?{}'.format(new_uri)
    else:
        return '?{}&page={}'.format(uri, page_obj.next_page_number())


@register.simple_tag(name='previous_pagination', takes_context=True)
def previous_pagination(context):
    """La paginación se hace en función de si tiene un query en GET.

    Para paginación, pagina previa si existe.

    Example:
        <a href="{% previous_pagination %}">previous</a>

    Si en el query de una URI existe ?page=xx, cambiara solo la parte
    del ?page=xxx por el nuevo numero de pagina. En caso contrario,
    añadirá page=xxx al query string.
    """
    request = context['request']
    page_obj = context['page_obj']
    uri = request.GET.urlencode()
    if not uri:
        return '?page={}'.format(page_obj.previous_page_number())
    if 'page' in uri:
        page = 'page={}'.format(page_obj.number)
        new_uri = uri.replace(page, 'page={}'.format(page_obj.previous_page_number()))
        return '?{}'.format(new_uri)
    else:
        return '?{}&page={}'.format(uri, page_obj.previous_page_number())
