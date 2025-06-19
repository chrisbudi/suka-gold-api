from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class user_notification(models.Model):
    user_notification_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user_notification_title = models.CharField(max_length=1000, blank=True, null=True)
    user_notification_description = models.TextField(blank=True, null=True)
    user_notification_date = models.DateTimeField(auto_now_add=True)
    user_notification_icon_type = models.CharField(
        max_length=100, default="info"
    )  # info, purchasing, warning
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
