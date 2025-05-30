from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class qris_webhook(models.Model):
    event = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    business_id = models.CharField(max_length=50)

    data_id = models.CharField(max_length=100)
    data_business_id = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    data_created = models.DateTimeField()
    qr_id = models.CharField(max_length=100)
    qr_string = models.TextField()
    reference_id = models.CharField(max_length=100)
    type = models.CharField(max_length=20)
    channel_code = models.CharField(max_length=20)
    expires_at = models.DateTimeField()

    # Metadata
    branch_code = models.CharField(max_length=100)

    # Payment detail
    receipt_id = models.CharField(max_length=50)
    source = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.reference_id} - {self.status}"
