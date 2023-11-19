from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import Schedule
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
                'amount': int(instance.amount_refund),
                'wallet_total': int(user.get_wallet().amount)
            }
        )


@receiver(post_save, sender=models.Spend)
def create_notification_spend(sender, instance, created, **kwargs):
    if created:
        user = instance.wallet.user
        NotificationUser.objects.create(
            type='SPENDING_WALLET',
            title=messages.SPENDING_WALLET.format(
                phonenumber=user.get_raw_phonenumber(),
                amount=instance.amount,
                number_id=instance.number_id),
            to_user=user,
            kwargs={
                'amount': int(instance.amount),
                'wallet_total': int(user.get_wallet().amount)
            }
        )


@receiver(post_save, sender=models.ClubConfig)
def modify_schedule_expire_transactions(sender, instance, created, **kwargs):
    if instance.discount_has_expire:
        Schedule.objects.create(
            name='schedule_task_check_expire_time_transactions',
            func='apps.club.tasks.delete_expired_transactions',
            schedule_type=Schedule.DAILY
        )
    else:
        Schedule.objects.filter(name='schedule_task_check_expire_time_transactions').delete()

