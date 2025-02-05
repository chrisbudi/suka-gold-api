from decimal import Decimal
import decimal
from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from user.models.users import user_props


class gold_saving_sell(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    gold_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    price = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal(0))
    gold_history_price_base = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    gold_history_price_sell = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    total_price = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    transaction_date = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Completed"
    )

    def __str__(self):
        return f"Gold Transaction {self.gold_transaction_id} - Type:"

    def update_status(self, status: str):
        self.status = status
        self.save()

    def save(self, *args, **kwargs):
        super(gold_saving_sell, self).save(*args, **kwargs)
        self.sell_gold()

    def sell_gold(self):
        userProps = user_props.objects.get(user=self.user)
        userProps.update_balance(self.total_price)
        userProps.update_gold_amt(self.weight * -1)


# Create your models here.
# buy, sell, buyback, sellback, transfer
class gold_saving_buy(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    gold_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    price = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal(0))
    gold_history_price_base = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    gold_history_price_buy = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )

    total_price = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    transaction_date = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Completed"
    )

    def __str__(self):
        return f"Gold Transaction {self.gold_transaction_id} - Type:"

    def update_status(self, status: str):
        self.status = status
        self.save()

    def save(self, *args, **kwargs):
        super(gold_saving_buy, self).save(*args, **kwargs)
        self.purchase_gold()

    def purchase_gold(self):
        userProps = user_props.objects.get(user=self.user)
        userProps.update_balance(self.total_price * -1)
        userProps.update_gold_amt(self.weight)


class gold_transfer(models.Model):
    gold_transfer_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gold_transfers_from",
    )
    user_from_name = models.CharField(max_length=255)
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gold_transfers_to",
    )
    user_to_name = models.CharField(max_length=255)
    transfer_ref_number = models.CharField(max_length=255)
    transfer_member_datetime = models.DateTimeField(auto_created=True)
    transfer_member_gold_weight = models.DecimalField(max_digits=8, decimal_places=4)
    transfer_member_notes = models.TextField()

    def __str__(self):
        return f"Gold Transfer {self.gold_transfer_id} - Type:"


class gold_buy(models.Model):
    gold_buy_id = UUIDv7Field(primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"Gold Buy {self.gold_buy_id} - Type"


class user_gold_history(models.Model):
    user_gold_hitory_id = UUIDv7Field(primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"User Gold History {self.user_gold_hitory_id} "
