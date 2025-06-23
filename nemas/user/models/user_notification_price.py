from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer


# create enum for transaction types
class user_notification_price(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    user_notification_price_id = UUIDv7Field(
        primary_key=True, unique=True, editable=False
    )
    user_notification_price_buy = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )
    user_notification_price_sell = models.DecimalField(
        max_digits=16,
        decimal_places=2,
    )

    timestamps = models.DateTimeField(auto_now_add=True)

    user_notification_price_status = models.BooleanField(default=True)
