import decimal
from django.db import models
from django.conf import settings

from core.fields.base_user_history import BaseUserHistory
from core.fields.uuidv7_field import UUIDv7Field


class wallet(models.Model):
    id = UUIDv7Field(primary_key=True, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=16, decimal_places=2, default=decimal.Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def topup(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount


class wallet_history(BaseUserHistory):
    TRANSACTION_TYPES = (
        ("D", "Deposit"),
        ("W", "Withdrawal"),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)

    class Meta(BaseUserHistory.Meta):
        verbose_name = "Wallet History"
        verbose_name_plural = "Wallet Histories"
