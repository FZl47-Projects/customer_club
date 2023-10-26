from apps.core.utils import send_sms, get_host_url


class NotificationUser:

    @classmethod
    def handler_transaction_created(cls, notification, phonenumber):
        pattern = 'vuw7wzmuvtcaz42'
        send_sms(phonenumber, pattern, {
            'amount': notification.kwargs['amount']
        })


NOTIFICATION_USER_HANDLERS = {
    'TRANSACTION_CREATED': NotificationUser.handler_transaction_created,
}
