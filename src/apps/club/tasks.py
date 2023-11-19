from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth import get_user_model
from . import models

User = get_user_model()


def delete_expired_transactions():
    club_config = models.ClubConfig.objects.first()
    now = timezone.now()
    expire_transaction = now + timezone.timedelta(days=club_config.discount_expire_day)
    expire_last_spend = now - timezone.timedelta(days=club_config.discount_expire_day)
    users = User.normal_user.filter(is_active=True)
    for user in users:
        last_spend = user.get_last_spend()
        if (not last_spend) or (last_spend.created_at < expire_last_spend):

            transactions = user.get_transactions().exclude(expire_time=None).filter(expire_time__lt=expire_transaction)
            transactions.update(is_showing=False)

            total_amount = transactions.aggregate(t=Sum('amount'))['t']
            if not total_amount:
                continue
            wallet = user.get_wallet()
            wallet.amount = total_amount
            if wallet.amount < 0:
                wallet.amount = 0
            wallet.save()
