from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class gold_transaction(models.Model):
    gold_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)

    def __str__(self):
        return f"Gold Transaction {self.gold_transaction_id} - Type:"


class gold_transfer(models.Model):
    gold_transfer_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gold_transfers_from",
    )

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gold_transfers_to",
    )
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
