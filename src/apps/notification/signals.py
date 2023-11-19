import warnings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import NotificationUser
from . import sms


def handler_sms_notify(notification, phonenumber):
    handler_name = notification.type
    handler_pattern = sms.NOTIFICATION_USER_HANDLERS.get(handler_name, None)
    if not handler_pattern:
        return
    pattern = sms.SMS_PATTERNS.get(handler_name)
    if not pattern:
        warnings.warn("Warning - pattern not found")
        return
    handler_pattern(pattern, notification, phonenumber)


@receiver(post_save, sender=NotificationUser)
def handle_notification_user_notify(sender, instance, **kwargs):
    if instance.send_notify:
        user = instance.to_user
        phonenumber = user.phonenumber
        if phonenumber:
            handler_sms_notify(instance, phonenumber)
