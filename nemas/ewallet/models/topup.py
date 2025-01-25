from django.conf import settings

from django.db import models
from pytz import timezone
from core.domain.gold import gold
from core.domain.bank import bank
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class topup_transaction(models.Model):
    topup_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    create_date = models.DateTimeField(auto_now_add=True)

    topup_payment_method = models.CharField(max_length=255)

    topup_timestamp = models.DateTimeField(auto_now_add=True)
    topup_amount = models.DecimalField(max_digits=16, decimal_places=2)
    topup_total_amount = models.DecimalField(max_digits=16, decimal_places=2)
    topup_admin = models.DecimalField(max_digits=16, decimal_places=2)

    topup_payment_bank = models.ForeignKey(
        bank,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # id
    topup_payment_number = models.CharField(max_length=255)

    # reference id
    # #if va then external_id
    topup_payment_ref = models.CharField(max_length=255)

    # qris --> then add qr id code
    # #va --> then add id #bank transfer code
    topup_payment_ref_code = models.CharField(max_length=255)

    topup_payment_channel_code = models.CharField(max_length=40, null=True, blank=True)
    topup_payment_expires_at = models.DateTimeField(auto_now_add=True)

    topup_notes = models.TextField(default="")
    topup_status = models.CharField(
        max_length=255, default="PENDING"
    )  # pending, success, failed, cancelled
    update_user = models.CharField(max_length=255)
    update_date = models.DateTimeField(auto_now=True)
    update_user_id = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            self.update_user = user.username
            self.update_user_id = user.id
        super().save(*args, **kwargs)

    class Meta:
        app_label = "ewallet"

    def __str__(self):
        return f"TOPUP Transaction {self.topup_transaction_id} - Type:"
