from decimal import Decimal
from django.conf import settings

from django.db import models
from core.fields.base_user_history import BaseUserHistory
from core.fields.uuidv7_field import UUIDv7Field


class gold_stock(models.Model):
    id = UUIDv7Field(primary_key=True, editable=False)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=16, decimal_places=4, default=Decimal(0.00))
    process_stock = models.DecimalField(
        max_digits=16, decimal_places=4, default=Decimal(0.00)
    )

    def add_gold(self, grams):
        self.topup_stock += grams

    def move_to_process(self, grams):
        if self.topup_stock < grams:
            raise ValueError("Not enough top-up stock")
        self.topup_stock -= grams
        self.process_stock += grams

    def reduce_gold(self, grams):
        if self.topup_stock >= grams:
            self.topup_stock -= grams
        elif self.topup_stock + self.process_stock >= grams:
            remaining = grams - self.topup_stock
            self.topup_stock = 0
            self.process_stock -= remaining
        else:
            raise ValueError("Not enough gold to sell")


class gold_history(BaseUserHistory):
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


class gold_deposito_history(BaseUserHistory):
    price_base = models.DecimalField(max_digits=10, decimal_places=2)
    price_sell = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    amount_dividend = models.DecimalField(max_digits=16, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=4)
    weight_dividend = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta(BaseUserHistory.Meta):
        verbose_name = "Gold Deposito History"
        verbose_name_plural = "Gold Deposito Histories"


class gold_loan_history(BaseUserHistory):
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


class gold_stock_history(BaseUserHistory):
    MOVEMENT_TYPES = (
        ("IN", "Stock In"),
        ("OUT", "Stock Out"),
    )
    id = UUIDv7Field(primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gold_stock_histories",
    )
    stock = models.ForeignKey(
        gold_stock, on_delete=models.CASCADE, related_name="histories"
    )
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    weight = models.DecimalField(max_digits=16, decimal_places=4)
    stock_before = models.DecimalField(
        max_digits=16, decimal_places=4, default=Decimal(0)
    )
    stock_after = models.DecimalField(
        max_digits=16, decimal_places=4, default=Decimal(0)
    )
    note = models.TextField(blank=True, null=True)

    class Meta(BaseUserHistory.Meta):
        verbose_name = "Gold Stock History"
        verbose_name_plural = "Gold Stock Histories"
