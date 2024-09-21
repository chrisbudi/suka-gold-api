from django.conf import settings

from django.contrib.auth.management import create_permissions
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)


from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django_ulid.models import ULIDField
from core.models.address import city
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.

class user_manager(BaseUserManager):
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

class user(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    """
    id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    pin = models.CharField(max_length=6)
    
    create_time = models.CharField(max_length=255)
    create_user = models.CharField(max_length=255)

    objects = user_manager()

    USERNAME_FIELD = 'email'
    
    class Meta:
        indexes = [
            models.Index(fields=['id', 'email']),
        ]
        
class user_props(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    city = models.ForeignKey(
        city,
        on_delete=models.CASCADE,
    )

    # make user id as primary key
    id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    wallet_amt = models.DecimalField(max_digits=12, decimal_places=2)
    gold_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    gold_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    invest_gold_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    loan_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    loan_amt = models.DecimalField(max_digits=12, decimal_places=2)
    photo = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    rek_number = models.CharField(max_length=255)
    npwp = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    address_post_code = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_created=True)
    create_user = models.CharField(max_length=255)

class user_ktp(models.Model):
    user = models.OneToOneField(
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
