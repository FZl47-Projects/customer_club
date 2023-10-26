from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import NotificationUser
from . import sms


def handler_sms_notify(notification, phonenumber):
    handler_pattern = sms.NOTIFICATION_USER_HANDLERS.get(notification.type, None)
    if not handler_pattern:
        return
    handler_pattern(notification, phonenumber)


@receiver(post_save, sender=NotificationUser)
def handle_notification_user_notify(sender, instance, **kwargs):
    if instance.send_notify:
        user = instance.to_user
        phonenumber = user.phonenumber
        if phonenumber:
            handler_sms_notify(instance, phonenumber)


