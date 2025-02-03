from django.db import models
from django.contrib.auth.models import User
from core.fields.uuidv7_field import UUIDv7Field
from django.conf import settings


class user_gold_history(models.Model):
    id = UUIDv7Field(primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gold_history"
    )
    gold_purchase_date = models.DateTimeField(auto_now_add=True)
    gold_weight = models.DecimalField(max_digits=10, decimal_places=4)
    gold_history_price_base = models.DecimalField(max_digits=10, decimal_places=2)
    gold_history_price_buy = models.DecimalField(max_digits=10, decimal_places=2)
    gold_history_price_sell = models.DecimalField(max_digits=10, decimal_places=2)
    gold_history_type = models.CharField(max_length=1)
    gold_history_amount = models.DecimalField(max_digits=16, decimal_places=2)
    gold_history_note = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} - {self.gold_purchase_date} - {self.gold_history_amount}"


class user_wallet_history(models.Model):
    id = UUIDv7Field(primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet_history",
    )
    wallet_history_date = models.DateTimeField(auto_now_add=True)
    wallet_history_amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet_history_type = models.CharField(max_length=1)
    wallet_history_notes = models.CharField(max_length=255)

    def __str__(self):
        return (
            f"{self.user} - {self.wallet_history_date} - {self.wallet_history_amount}"
        )


class user_transfer_history(models.Model):
    id = UUIDv7Field(primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transfer_user",
    )
    trf_user_from_name = models.CharField(max_length=255)
    trf_history_date = models.DateTimeField(auto_now_add=True)
    trf_history_amount = models.DecimalField(max_digits=8, decimal_places=4)
    trf_user_to_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transfer_from",
    )
    trf_user_to_name = models.CharField(max_length=255)
    trf_ref_number = models.CharField(max_length=255)
    trf_history_notes = models.CharField(max_length=255)
    trf_type = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.user} "
