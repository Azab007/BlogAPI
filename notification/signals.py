# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from post.models import Comment

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        post_author = instance.post.author
        Notification.objects.create(user=post_author, message=f'New comment on your post: {instance.text}')
