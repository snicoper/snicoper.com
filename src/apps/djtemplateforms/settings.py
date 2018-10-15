from django.conf import settings

DJTEMPLATEFORMS_DEFAULT_TEMPLATE = getattr(
    settings, 'DJTEMPLATEFORMS_DEFAULT_TEMPLATE', 'bootstrap4'
)
