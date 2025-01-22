from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class topup_transaction(models.Model):
    topup_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    topup_timestamp = models.DateTimeField(auto_created=True)
    topup_amount = models.DecimalField(max_digits=16, decimal_places=2)
    topup_cost = models.DecimalField(max_digits=16, decimal_places=2)
    topup_payment_method = models.CharField(max_length=255)
    topup_payment_number = models.CharField(max_length=255)
    topup_payment_ref = models.CharField(max_length=255)
    topup_notes = models.TextField()
    topup_status = models.CharField(max_length=255)

    def __str__(self):
        return f"TOPUP Transaction {self.topup_transaction_id} - Type:"
