from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from core.domain.address import postal_code
from core.domain import gold, gold_price_config, gold_cert_price
from order.models import order_gold


class order_tracking(models.Model):
    order_tracking_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_gold_id = models.ForeignKey(
        order_gold,
        on_delete=models.CASCADE,
    )
    tracking_timestamp = models.DateTimeField(auto_created=True)
    tracking_number = models.CharField(max_length=50)
    tracking_status = models.CharField(max_length=50)
    tracking_notes = models.CharField(max_length=100)
