import uuid
from django.db import models
from django.conf import settings

from core.fields import uuidv7_field
from core.fields.base_user_history import BaseUserHistory


class GoldHistory(BaseUserHistory):
    TRANSACTION_TYPES = (
        ("B", "Buy"),
        ("S", "Sell"),
    )
    weight = models.DecimalField(max_digits=10, decimal_places=4)
    price_base = models.DecimalField(max_digits=10, decimal_places=2)
    price_buy = models.DecimalField(max_digits=10, decimal_places=2)
    price_sell = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta(BaseUserHistory.Meta):
        verbose_name = "Gold History"
        verbose_name_plural = "Gold Histories"

    @classmethod
    def for_user(cls, user):
        return cls.objects.filter(user=user)

    @classmethod
    def for_user_and_date_range(cls, user, start_date, end_date):
        return cls.objects.filter(user=user, date__range=(start_date, end_date))

    @classmethod
    def for_user_and_type(cls, user, transaction_type):
        return cls.objects.filter(user=user, transaction_type=transaction_type)


class WalletHistory(BaseUserHistory):
    TRANSACTION_TYPES = (
        ("D", "Deposit"),
        ("W", "Withdrawal"),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)

    class Meta(BaseUserHistory.Meta):
        verbose_name = "Wallet History"
        verbose_name_plural = "Wallet Histories"


class GoldDepositoHistory(BaseUserHistory):
    price_base = models.DecimalField(max_digits=10, decimal_places=2)
    price_sell = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    amount_dividend = models.DecimalField(max_digits=16, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=4)
    weight_dividend = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta(BaseUserHistory.Meta):
        verbose_name = "Gold Deposito History"
        verbose_name_plural = "Gold Deposito Histories"


class GoldLoanHistory(BaseUserHistory):
    price_base = models.DecimalField(max_digits=10, decimal_places=2)
    price_sell = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=4)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=16, decimal_places=2)
    loan_amount = models.DecimalField(max_digits=16, decimal_places=2)
    admin_fee = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta(BaseUserHistory.Meta):
        verbose_name = "Gold Loan History"
        verbose_name_plural = "Gold Loan Histories"
