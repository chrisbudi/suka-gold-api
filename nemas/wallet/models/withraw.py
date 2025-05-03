from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class withraw_transaction(models.Model):
    withdraw_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    withdraw_number = models.CharField(max_length=100, blank=True, null=True)
    withdraw_timestamp = models.DateTimeField(auto_created=True)
    withdraw_amount = models.DecimalField(max_digits=16, decimal_places=2)
    withdraw_cost = models.DecimalField(max_digits=16, decimal_places=2)
    withdraw_payment_method = models.CharField(max_length=255)
    withdraw_payment_number = models.CharField(max_length=255)
    withdraw_payment_ref = models.CharField(max_length=255)
    withdraw_notes = models.TextField()
    withdraw_status = models.CharField(max_length=255)

    class meta:
        app_label = "wallet"

    def __str__(self):
        return f"withdraw Transaction {self.withdraw_number} - Type:"
