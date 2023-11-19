from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from apps.core.utils import random_str


class ClubInfo(models.Model):
    title = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title


class ClubConfig(models.Model):
    discount_percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_has_expire = models.BooleanField(default=True)
    discount_expire_day = models.IntegerField(default=30)

    def __str__(self):
        return 'club config'


class Wallet(models.Model):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'wallet - {self.user}'


class Transaction(models.Model):
    number_id = models.CharField(max_length=12, default=random_str)
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    amount_refund = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    discount_percentage = models.IntegerField()
    expire_time = models.DateTimeField(null=True)
    is_showing = models.BooleanField(default=True)

    class Meta:
        ordering = '-id',

    def save(self, *args, **kwargs):
        club_config = ClubConfig.objects.first()
        if not club_config:
            return
        if club_config.discount_has_expire:
            self.expire_time = timezone.now() + timezone.timedelta(days=club_config.discount_expire_day)
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f'#{self.id} - {self.wallet}'

    @classmethod
    def get_amount_refund(cls, amount):
        dp = cls.get_discount_percentage()
        try:
            return (amount / 100) * dp
        except ZeroDivisionError:
            return 0

    @classmethod
    def get_discount_percentage(cls):
        c = ClubConfig.objects.first()
        if not c:
            return 0
        return c.discount_percentage


class Spend(models.Model):
    number_id = models.CharField(max_length=12, default=random_str)
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = '-id',

    def __str__(self):
        return f'#{self.id} - {self.wallet}'
