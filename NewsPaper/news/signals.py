from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import send_notifications


@receiver(m2m_changed, sender=PostCategory)
def add_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subs_email = []
        for cat in categories:
            subs = cat.subscribers.all()
            subs_email += [s.email for s in subs]

        send_notifications.delay(instance.text, instance.pk, instance.title, subs_email)
