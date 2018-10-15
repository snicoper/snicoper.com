from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from ..settings import DJTEMPLATEFORMS_DEFAULT_TEMPLATE as DEFAULT_TEMPLATE

register = template.Library()


@register.simple_tag
def form(form_class, **field_extras):
    """Renderiza un form completo."""
    html = hidden_fields(form_class)
    html += non_field_errors(form_class)
    for field in form_class:
        html += form_field(field, **field_extras)
    return mark_safe(html)


@register.simple_tag
def hidden_fields(form_class):
    """Renderiza los campos ocultos del formulario."""
    hidden_template = 'djtemplateforms/{}/hidden.html'.format(DEFAULT_TEMPLATE)
    return render_to_string(hidden_template, {'form': form_class})


@register.simple_tag
def non_field_errors(form_class):
    """Renderiza errores globales del formulario ."""
    form_errors_template = 'djtemplateforms/{}/form_errors.html'.format(DEFAULT_TEMPLATE)
    return render_to_string(form_errors_template, {'form': form_class})


@register.simple_tag
def form_field(field, **field_extras):
    """Renderiza un campo de un formulario.

    Si field no existe, return un string vacío.
    """
    if not field:
        return ''
    widget_name = _widget_name(field)
    field_extras = _widget_type(widget_name, **field_extras)
    field_extras['field'] = field
    field_extras['attrs'] = field.field.widget.attrs
    field_extras['widget_name'] = widget_name
    field_extras['attrs_file'] = 'djtemplateforms/{}/attrs.html'.format(DEFAULT_TEMPLATE)
    if widget_name == 'HiddenInput':
        return ''
    return _render(field_extras['template_name'], field_extras)


def _widget_name(field):
    """Obtener el nombre de un widget."""
    return field.field.widget.__class__.__name__


def _render(template_name, field_extras):
    """Renderiza un field de formulario."""
    template_dir = 'djtemplateforms/{}/{}'.format(DEFAULT_TEMPLATE, template_name)
    return render_to_string(template_dir, field_extras)


def _widget_type(widget_name, **field_extras):
    """Obtener el tipo del widget y añade el template asociado según el type."""
    template_name = 'input.html'
    ftype = 'text'
    if widget_name == 'Textarea':
        template_name = 'text.html'
    if widget_name == 'Select' or widget_name == 'SelectMultiple':
        template_name = 'select.html'
    if widget_name == 'CheckboxInput' or widget_name == 'CheckboxSelectMultiple':
        template_name = 'checkbox.html'
        ftype = 'checkbox'
    if widget_name == 'RadioSelect':
        template_name = 'radio.html'
        ftype = 'radio'
    if widget_name == 'FileInput' or widget_name == 'ClearableFileInput':
        template_name = 'file.html'
        ftype = 'file'
    if widget_name == 'TextInput':
        template_name = 'input.html'
        ftype = 'text'
    if widget_name == 'PasswordInput':
        ftype = 'password'
    if widget_name == 'NumberInput':
        ftype = 'number'
    if widget_name == 'EmailInput':
        ftype = 'email'
    if widget_name == 'URLInput':
        ftype = 'url'
    if widget_name == 'DateTimeInput' or widget_name == 'DateInput':
        ftype = 'date'
    field_extras['ftype'] = ftype
    field_extras['template_name'] = template_name
    return field_extras
