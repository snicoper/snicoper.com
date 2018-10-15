from django.conf import settings
from django.contrib.sites.models import Site

from contact.models import ContactMessage


def common_template_vars(request):
    return {
        'SITE': Site.objects.get_current(),
        'PROTOCOL': 'https://' if request.is_secure() else 'http://',
        'DISQUS_SHORTNAME': getattr(settings, 'DISQUS_SHORTNAME', False),
        'ADSENSE_IMAGES_FAKE': getattr(settings, 'ADSENSE_IMAGES_FAKE', False),
        'CONTACT_MESSAGES_UNREAD': ContactMessage.objects.filter(read=False).count()
    }
