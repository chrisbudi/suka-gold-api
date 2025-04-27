from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from core.domain.address import postal_code
from core.domain import gold, gold_cert_detail_price
from order.models import order_gold, order_gold_detail


class order_dispatch(models.Model):
    order_dispatch_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_dispatch_number = models.CharField(max_length=50)
    order_gold_id = models.ForeignKey(
        order_gold,
        on_delete=models.CASCADE,
    )

    dispatch_timestamp = models.DateTimeField(auto_created=True)
    order_gold_number = models.CharField(max_length=50)
    order_shipping = models.ForeignKey(
        "order_shipping",
        on_delete=models.CASCADE,
    )
    order_dispatch_status = models.CharField(max_length=50)


class order_dispatch_detail(models.Model):
    order_dispatch_detail_id = UUIDv7Field(
        primary_key=True, unique=True, editable=False
    )
    order_dispatch_id = models.ForeignKey(
        order_dispatch,
        on_delete=models.CASCADE,
    )
    order_gold_detail = models.ForeignKey(
        order_gold_detail,
        on_delete=models.CASCADE,
    )
    gold = models.ForeignKey(
        gold,
        on_delete=models.CASCADE,
    )
    gold_cert_detail_price = models.ForeignKey(
        gold_cert_detail_price,
        on_delete=models.CASCADE,
    )
    gold_cert_code = models.CharField(max_length=50)
