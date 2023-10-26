from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from jsonfield import JSONField

User = get_user_model()


def upload_notification_src(instance, path):
    frmt = str(path).split('.')[-1]
    return f'images/notifications/{get_random_string(20)}.{frmt}'


class NotificationUser(models.Model):
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    kwargs = JSONField(null=True, blank=True)
    send_notify = models.BooleanField(default=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    # show for user or not
    is_showing = models.BooleanField(default=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'notification for {self.to_user}'

    def get_title(self):
        return f'{self.to_user} - {self.title}'

