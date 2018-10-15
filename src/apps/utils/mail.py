from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template, render_to_string


def send_templated_mail(subject, from_email, recipients, context,
                        template_text, template_html=None, **kwargs):
    """Enviá un email usando EmailMultiAlternatives con templates text y html (opcional).

    Hace exactamente lo mismo que EmailMultiAlternatives, pero a diferencia,
    require de un contexto y un template .txt y otro opcional .html.

    Si contiene template_html, el email sera mandado en HTML de lo
    contrario, se mandara solo en TXT.

    La diferencia con send_mail de Django es reply_to, también
    con este wrapper, la carga de plantillas es mas cómodo.

    Args:
        subject (str): Titulo del mensaje.
        from_email (str): Quien lo enviá.
        recipients (tuple|list): Recipientes.
        context (dict): Contexto para el template.
        template_text (str): Template .txt a usar en el mensaje.
        template_html (str): Template .html a usar en el mensaje.
        kwargs (dict): kwargs para EmailMultiAlternatives.

    Returns:
        (bool): True en caso de éxito, False en caso contrario.

    Raises:
        Lanzara los que EmailMultiAlternatives pueda lanzar o en
        caso de no existir los templates.
    """
    content_text = render_to_string(template_text, context)
    email = EmailMultiAlternatives(
        subject=subject,
        body=content_text,
        from_email=from_email,
        to=recipients,
        **kwargs
    )
    if template_html:
        html_content = get_template(template_html).render(context)
        email.attach_alternative(html_content, 'text/html')
    return email.send()
