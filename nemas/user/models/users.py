from django.conf import settings

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.db import models, transaction
from django.contrib.auth.models import PermissionsMixin
from core.domain.address import city
from core.fields.uuidv7_field import UUIDv7Field
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

from decimal import Decimal
from user.models.user_history import user_wallet_history, user_gold_history


# Create your models here.
class user_manager(BaseUserManager):
    """Managers for users"""

    @transaction.atomic
    def create_user(
        self,
        user_name=None,
        email=None,
        phone_number=None,
        password=None,
        name=None,
        **extra_fields,
    ):
        """Create and return a new user"""
        if not email and not phone_number:
            raise ValueError("the user must have either an email or phone number")

        user = self.model(
            user_name=user_name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            name=name,
            **extra_fields,
        )
        user.set_password(password)
        user.create_time = datetime.now()
        user.save(using=self._db)

        # create user props data
        user_props.objects.create(
            user=user,
            wallet_amt=0,
            gold_wgt=0,
            invest_gold_wgt=0,
            loan_wgt=0,
            loan_amt=0,
            photo="",
            bank_account_code="",
            bank_account_number="",
            bank_account_holder_name="",
            level="",
            address="",
            address_post_code="",
            create_user="system",
            create_time=datetime.now(),
            update_user="system",
            update_time=datetime.now(),
        )

        return user

    def create_superuser(
        self,
        user_name=None,
        email=None,
        phone_number=None,
        password=None,
        name=None,
        **extra_fields,
    ):
        """Create and return a new user"""
        user = self.create_user(
            user_name, email, phone_number, password, name, **extra_fields
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class user(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username
    """

    id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    user_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    user_type = models.CharField(max_length=100, default="user")
    # unverified, verify KTP, verify Photo, verified, rejected, blacklisted
    verify_status = models.CharField(max_length=100, default="unverified")
    verify_updated_time = models.DateTimeField(null=True, blank=True)
    verify_notes = models.TextField(null=True, blank=True)
    photo_selfie_url = models.CharField(max_length=255, null=True, blank=True)
    photo_ktp_url = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    pin = models.IntegerField(
        validators=[
            MaxValueValidator(999999),
            MinValueValidator(100000),
        ],
        null=True,
        blank=True,
    )

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=256)

    update_time = models.DateTimeField(auto_now=True)
    update_user = models.CharField(max_length=256)

    objects = user_manager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_name", "phone_number"]

    def has_perm(self, perm: str, obj: None = None) -> bool:
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label: str) -> bool:
        return super().has_module_perms(app_label)

    def verify_update_state(self, status: str):
        self.verify_status = status
        self.verify_updated_time = datetime.now()
        self.update_time = datetime.now()
        self.save()

    def verify_update_fail_notes(self, notes: str):
        self.verify_notes = notes
        self.update_time = datetime.now()
        self.save()

    def __str__(self):
        return self.id

    class Meta:
        indexes = [
            models.Index(fields=["id", "email", "user_name"]),
        ]


class user_props(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_props"
    )

    city = models.ForeignKey(
        city,
        on_delete=models.CASCADE,
        null=True,
    )

    # make user id as primary key
    id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    wallet_amt = models.DecimalField(max_digits=12, decimal_places=2)
    gold_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    invest_gold_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    loan_wgt = models.DecimalField(max_digits=10, decimal_places=4)
    loan_amt = models.DecimalField(max_digits=12, decimal_places=2)
    photo = models.CharField(max_length=255)
    bank_account_code = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=255)
    bank_account_holder_name = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    level_id = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255)
    address_post_code = models.CharField(max_length=255)
    income_source = models.CharField(max_length=255, blank=True, null=True)
    investment_purpose = models.CharField(max_length=255, blank=True, null=True)
    referal_code = models.CharField(max_length=10, blank=True, null=True)
    create_user = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_user = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now=True)

    def update_balance(self, amount: Decimal):
        print(f"amount: {amount}")
        self.wallet_amt += Decimal(amount)
        print(f"wallet_amt: {self.wallet_amt}")
        self.save()

        # insert history user amount
        user_wallet_history.objects.create(
            user=self.user,
            wallet_history_amount=amount,
            wallet_history_type="C",
            wallet_history_notes="Topup",
        )

    def update_gold_amt(self, weight: Decimal):
        self.gold_wgt += Decimal(weight)
        self.save()

    def validate_balance(self, amount: Decimal):
        userProps = user_props.objects.get(user=self.user)
        if userProps.wallet_amt < amount:
            return False
        return True

    def validate_weight(self, weight: Decimal):
        userProps = user_props.objects.get(user=self.user)
        if userProps.gold_wgt < weight:
            return False
        return True


class user_virtual_account(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    va_number = models.CharField(max_length=50)
    bank = models.CharField(max_length=50)
    merchant_code = models.CharField(max_length=50)

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=100)
    create_user_id = models.CharField(max_length=50)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.CharField(max_length=100)
    update_user_id = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            if not self.pk:
                self.create_user = user.username
                self.create_user_id = user.id
            self.update_user = user.username
            self.update_user_id = user.id
        super().save(*args, **kwargs)


class user_address(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    subdistrict = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=255)
    update_time = models.DateTimeField(auto_now=True)
    update_user = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            if not self.pk:
                self.create_user = user.username
            self.update_user = user.username
        super().save(*args, **kwargs)


class user_ktp(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    nik = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    place_of_birth = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    administrative_village = models.CharField(max_length=255)
    blood_type = models.CharField(max_length=3, default="-")
    gender = models.CharField(max_length=255)
    religion = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    nationality = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=255, blank=True, null=True)
    create_user = models.CharField(max_length=255, blank=True, null=True)
    updated_time = models.DateTimeField(auto_now=True)
    updated_user = models.CharField(max_length=255, blank=True, null=True)
