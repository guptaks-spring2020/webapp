import uuid
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyAccountManager(BaseUserManager):

    def create_user(self, email_address, password=None, ):
        if not email_address:
            raise ValueError('Users must have an email_address address')

        user = self.model(email_address=self.normalize_email_address(email_address))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, password, ):
        user = self.create_user(email_address=self.normalize_email_address(email_address), password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email_address = models.EmailField(verbose_name='email_address', max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    account_created = models.DateTimeField(verbose_name='account created', auto_now_add=True)
    account_updated = models.DateTimeField(verbose_name='account updated', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email_address'

    objects = MyAccountManager()

    def __str__(self):
        return self.email_address

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
