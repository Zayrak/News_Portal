
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Post
from .tasks import new_post_subscription


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, **kwargs):
    print(F'Post start...')
    new_post_subscription(instance)
