from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class disburst_transaction(models.Model):
    disburst_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    disburst_number = models.CharField(max_length=100, blank=True, null=True)

    disburst_timestamp = models.DateTimeField(auto_created=True)
    disburst_amount = models.DecimalField(max_digits=16, decimal_places=2)
    disburst_admin = models.DecimalField(max_digits=16, decimal_places=2)
    disburst_total_amount = models.DecimalField(max_digits=16, decimal_places=2)
    disburst_payment_bank_code = models.CharField(max_length=255)
    disburst_payment_bank_number = models.CharField(max_length=255)
    disburst_payment_bank_account_holder_name = models.CharField(max_length=255)
    disburst_status = models.CharField(max_length=255)
    disburst_payment_ref = models.CharField(max_length=255)

    def __str__(self):
        return f"disburst Transaction {self.disburst_transaction_id} - Type:"
