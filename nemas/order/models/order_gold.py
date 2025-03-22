from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from core.domain import (
    gold,
    gold_price_config,
    cert,
    delivery_partner,
    delivery_partner_service,
    payment_method,
)
from core.domain.delivery import delivery_partner_service
from order.models.order_cart import order_cart_detail
from user.models.users import user_address


class order_gold(models.Model):
    order_gold_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_number = models.CharField(max_length=255)
    order_timestamp = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    order_user_address = models.ForeignKey(
        user_address,
        on_delete=models.CASCADE,
    )
    order_cart = models.ForeignKey(
        "order_cart",
        on_delete=models.CASCADE,
        null=True,
    )

    order_phone_number = models.CharField(max_length=255)
    order_item_weight = models.DecimalField(max_digits=10, decimal_places=4)

    order_payment_method = models.ForeignKey(
        payment_method, on_delete=models.CASCADE, null=True
    )

    order_payment_va_bank = models.CharField(max_length=255, null=True)
    order_payment_va_number = models.CharField(max_length=255, null=True)

    order_amount = models.DecimalField(max_digits=16, decimal_places=2)
    order_admin_amount = models.DecimalField(max_digits=16, decimal_places=2)

    order_pickup_address = models.CharField(max_length=255, null=True, blank=True)
    order_pickup_customer_datetime = models.DateTimeField(null=True, blank=True)

    order_tracking_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    order_tracking_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    order_tracking_packing = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    order_tracking_insurance_admin = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    order_tracking_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    order_gold_payment_ref = models.CharField(max_length=255, null=True)
    order_gold_payment_status = models.CharField(max_length=255, null=True)
    order_promo_code = models.CharField(max_length=255, null=True)

    order_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_total_price = models.DecimalField(max_digits=16, decimal_places=2)

    tracking_status_id = models.CharField(max_length=255, null=True)
    tracking_status = models.CharField(max_length=255, null=True)

    tracking_courier = models.ForeignKey(
        delivery_partner, on_delete=models.CASCADE, null=True
    )

    tracking_courier_service = models.ForeignKey(
        delivery_partner_service, on_delete=models.CASCADE, null=True
    )
    tracking_number = models.CharField(max_length=255, null=True)
    tracking_last_note = models.CharField(max_length=255, null=True)
    tracking_last_updated_datetime = models.DateTimeField(auto_created=True, null=True)
    tracking_sla = models.DateTimeField(auto_created=True, null=True)

    def __str__(self):
        return f"Gold Transaction {self.order_gold_id} - Type:"

    def create(self, validated_data):
        validated_data["order_number"] = self.generate_number()
        return order_gold.objects.create(**validated_data)

    def update_status(self, status: str):
        self.tracking_status = status
        self.save()

    def generate_number(self):
        return UUIDv7Field()


class order_gold_detail(models.Model):
    order_gold_detail_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_gold = models.ForeignKey(
        order_gold,
        on_delete=models.CASCADE,
    )
    gold = models.ForeignKey(
        gold,
        on_delete=models.CASCADE,
    )
    order_cart_detail = models.ForeignKey(
        order_cart_detail,
        on_delete=models.CASCADE,
        null=True,
    )
    gold_type = models.CharField(max_length=255, null=True)
    gold_brand = models.CharField(max_length=255)
    gold_price = models.ForeignKey(
        gold_price_config, on_delete=models.CASCADE, null=True
    )
    cert = models.ForeignKey(cert, on_delete=models.CASCADE, null=True)
    cert_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    order_weight = models.DecimalField(max_digits=10, decimal_places=4)
    order_qty = models.IntegerField()
    order_price = models.DecimalField(max_digits=16, decimal_places=2)
    order_cert_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_detail_total_price = models.DecimalField(max_digits=16, decimal_places=2)
