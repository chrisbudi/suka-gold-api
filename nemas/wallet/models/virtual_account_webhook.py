from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class virtual_account_webhook(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)
    callback_virtual_account_id = models.CharField(max_length=100)
    owner_id = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    bank_code = models.CharField(max_length=20)
    amount = models.IntegerField()
    transaction_timestamp = models.DateTimeField()
    merchant_code = models.CharField(max_length=50)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    def __str__(self):
        return self.payment_id
