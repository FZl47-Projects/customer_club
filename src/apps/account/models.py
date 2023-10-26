from django.db import models
from django.urls import reverse
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from apps.club.models import Wallet


class CustomBaseUserManager(BaseUserManager):

    def create_user(self, phonenumber, password, email=None, **extra_fields):
        """
        Create and save a normal_user with the given phonenumber and password.
        """
        if not phonenumber:
            raise ValueError("The phonenumber must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, phonenumber=phonenumber, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phonenumber, password, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(phonenumber=phonenumber, password=password, role='admin_user', email=email,
                                **extra_fields)


class NormalUserManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(role='normal_user')


class User(AbstractUser):
    ROLE_USER_OPTIONS = (
        ('normal_user', 'کاربر عادی'),
        ('operator_user', 'کاربر اپراتور'),
        ('admin_user', 'کاربر ادمین'),
    )
    first_name = models.CharField("first name", max_length=150, null=True, blank=True, default="Unknown")
    last_name = models.CharField("last name", max_length=150, null=True, blank=True)
    username = None
    phonenumber = PhoneNumberField(region='IR', unique=True)
    # type users
    role = models.CharField(max_length=20, choices=ROLE_USER_OPTIONS, default='normal_user')

    USERNAME_FIELD = "phonenumber"
    REQUIRED_FIELDS = []

    objects = CustomBaseUserManager()
    normal_user = NormalUserManager()

    class Meta:
        ordering = '-id',

    @property
    def is_admin(self):
        return True if self.role == 'admin_user' else False

    @property
    def is_operator(self):
        return True if self.role == 'operator_user' else False

    def __str__(self):
        return f'{self.role} - {self.phonenumber}'

    def get_role_label(self):
        return self.get_role_display()

    def get_raw_phonenumber(self):
        p = str(self.phonenumber).replace('+98', '')
        return p

    def get_full_name(self):
        fl = f'{self.first_name or ""} {self.last_name or ""}'.strip() or 'Unknown'
        return fl

    def get_email(self):
        return self.email or '-'

    def get_last_login_formated(self):
        if self.last_login:
            return self.last_login.strftime('%Y-%m-%d %H:%M:%S')
        return '-'

    def get_number_id(self):
        return self.id

    def get_absolute_url(self):
        return reverse('account:user_detail', args=(self.id,))

    def get_wallet_amount(self):
        return self.get_wallet().amount

    def get_wallet(self):
        wallet = getattr(self, 'wallet', None)
        if not wallet:
            # create wallet
            wallet = Wallet.objects.create(user=self)
        return wallet

    def get_transactions(self):
        return self.get_wallet().transaction_set.all()
