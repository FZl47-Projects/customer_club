from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.notification.models import NotificationUser
from apps.notification import messages
from . import models


@receiver(post_save, sender=models.Transaction)
def create_notification_transaction(sender, instance, created, **kwargs):
    if created:
        user = instance.wallet.user
        NotificationUser.objects.create(
            type='TRANSACTION_CREATED',
            title=messages.TRANSACTION_CREATED.format(
                phonenumber=user.get_raw_phonenumber(),
                amount=instance.amount_refund,
                number_id=instance.number_id),
            to_user=user,
            kwargs={
                'amount':instance.amount_refund
            }
        )
