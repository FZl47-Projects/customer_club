from django.conf import settings
from apps.core.utils import send_sms, get_host_url

SMS_PATTERNS = settings.SMS_CONFIG['PATTERNS']


class NotificationUser:

    @classmethod
    def handler_transaction_created(cls, pattern, notification, phonenumber):
        send_sms(phonenumber, pattern, {
            'amount': str(notification.kwargs['amount']),
            'wallet_total': str(notification.kwargs['wallet_total'])
        })

    @classmethod
    def handler_spending_wallet(cls, pattern, notification, phonenumber):
        send_sms(phonenumber, pattern, {
            'amount': str(notification.kwargs['amount']),
            'wallet_total': str(notification.kwargs['wallet_total'])
        })


NOTIFICATION_USER_HANDLERS = {
    'TRANSACTION_CREATED': NotificationUser.handler_transaction_created,
    'SPENDING_WALLET': NotificationUser.handler_spending_wallet,
}
