from django.conf import settings

from django.contrib.auth.management import create_permissions
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)


# Create your models here.

class UserManager(BaseUserManager):
    """Managers for users"""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    """
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    pin = models.CharField(max_length=6)
    wallet_amt = models.DecimalField(max_digits=5, decimal_places=2)    
    gold_wgt = models.DecimalField(max_digits=5, decimal_places=2)
    invest_gold_wgt = models.CharField(max_length=255)
    loan_wgt = models.CharField(max_length=255)
    loan_amt = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    rek_number = models.CharField(max_length=255)
    npwp = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    city_id = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_post_code = models.CharField(max_length=255)
    create_time = models.CharField(max_length=255)
    create_user = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class UserKtp(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    ktp_number = models.CharField(max_length=255)
    ktp_photo = models.CharField(max_length=255)
    ktp_address = models.CharField(max_length=255)
    ktp_address_post_code = models.CharField(max_length=255)
    ktp_city_id = models.CharField(max_length=255)
    ktp_create_time = models.CharField(max_length=255)
    ktp_create_user = models.CharField(max_length=255)
