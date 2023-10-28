import warnings
from django.conf import settings
from apps.core.utils import send_sms, get_host_url

SMS_PATTERNS = settings.SMS_CONFIG['PATTERNS']


class NotificationUser:

    @classmethod
    def handler_transaction_created(cls, notification, phonenumber):
        handler_name = 'TRANSACTION_CREATED'
        pattern = SMS_PATTERNS.get(handler_name)
        if not pattern:
            warnings.warn("Warning - pattern not found")
        send_sms(phonenumber, pattern, {
            'amount': notification.kwargs['amount']
        })


NOTIFICATION_USER_HANDLERS = {
    'TRANSACTION_CREATED': NotificationUser.handler_transaction_created,
}
