import logging

from django.conf import settings
from django.template import loader, Context
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site


def send_email(recipients, subject, sender, text_template_name, html_template_name, context, bcc=None, reply_to=None, attachments=None):
    """ Attachments should be a list of tuples. Tuple format:
        ("filename", "content", "mimetype")
    """
    text_template = loader.get_template(text_template_name)
    html_template = loader.get_template(html_template_name)

    site = Site.objects.get(pk=getattr(settings, 'SITE_ID', 1))
    context['https_domain'] = 'https://%s' % site.domain
    email_kwargs = {
        'subject': subject,
        'body': text_template.render(Context(context)),
        'from_email': sender,
    }

    if bcc:
        email_kwargs['to'] = [sender]
        email_kwargs['bcc'] = recipients
    else:
        email_kwargs['to'] = recipients

    headers = {}
    if reply_to is not None:
        headers['Reply-To'] = reply_to

    if headers:
        email_kwargs['headers'] = headers

    if attachments:
        email_kwargs['attachments'] = attachments

    msg = EmailMultiAlternatives(**email_kwargs)
    msg.content_subtype = "text"
    msg.attach_alternative(
        html_template.render(Context(context)), "text/html")

    msg.send()

