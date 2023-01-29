from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory


def send_notifications(text, pk, title, subs_email):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': text,
            'link': f'{settings.SITE_URL}/post/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subs_email
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def add_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subs_email = []
        for cat in categories:
            subs = cat.subscribers.all()
            subs_email += [s.email for s in subs]

        send_notifications(instance.text, instance.pk, instance.title, subs_email)


