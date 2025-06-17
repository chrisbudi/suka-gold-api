from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class user_level_history(models.Model):
    user_level_history_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user_level_name = models.CharField(max_length=100, blank=True, null=True)
    user_level_transaction_amount = models.DecimalField(
        max_digits=16, decimal_places=2, default=0
    )
    user_level_transaction_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    user_level_status = models.CharField(
        max_length=255, default="PENDING"
    )  # pending, success, failed, cancelled
