from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from core.domain.address import postal_code
from gold_transaction.domain.models.order_gold import order_gold
from core.domain import gold, gold_price_config, gold_cert_price


class order_gold(models.Model):
    order_gold_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_number = models.CharField(max_length=255)
    order_timestamp = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    order_address = models.CharField(max_length=255)
    order_post_code = models.ForeignKey(
        postal_code,
        on_delete=models.CASCADE,
    )
    order_postal_code = models.CharField(max_length=255)
    order_phone_number = models.CharField(max_length=255)
    order_item_weight = models.DecimalField(max_digits=10, decimal_places=4)
    order_amount = models.DecimalField(max_digits=16, decimal_places=2)
    order_tracking_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_promo_code = models.CharField(max_length=255)
    order_discount = models.DecimalField(max_digits=10, decimal_places=2)
    order_total_price = models.DecimalField(max_digits=16, decimal_places=2)
    tracking_status_id = models.CharField(max_length=255)
    tracking_status = models.CharField(max_length=255)
    tracking_courier = models.CharField(max_length=255)
    tracking_number = models.CharField(max_length=255)
    tracking_last_note = models.CharField(max_length=255)
    tracking_last_updated_datetime = models.DateTimeField(auto_created=True)
    tracking_sla = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f"Gold Transaction {self.order_gold_id} - Type:"


class order_gold_detail(models.Model):
    order_gold_detail_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_gold_id = models.ForeignKey(
        order_gold,
        on_delete=models.CASCADE,
    )
    gold_id = models.ForeignKey(
        gold,
        on_delete=models.CASCADE,
    )
    gold_type = models.CharField(max_length=255)
    gold_brand = models.CharField(max_length=255)
    certificate_number = models.CharField(max_length=255)
    gold_price_id = models.ForeignKey(
        gold_price_config,
        on_delete=models.CASCADE,
    )
    cert_price_id = models.ForeignKey(
        gold_cert_price,
        on_delete=models.CASCADE,
    )
    order_qty = models.IntegerField()
    order_price = models.DecimalField(max_digits=16, decimal_places=2)
    order_cert_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_detail_total_price = models.DecimalField(max_digits=16, decimal_places=2)
