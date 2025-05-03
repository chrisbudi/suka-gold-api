from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from core.domain.address import postal_code
from core.domain import delivery_partner
from order.models import order_gold


class order_shipping(models.Model):
    order_delivery_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_gold_id = models.ForeignKey(
        order_gold,
        on_delete=models.CASCADE,
    )
    delivery_partner_id = models.ForeignKey(
        delivery_partner,
        on_delete=models.CASCADE,
    )
    delivery_price = models.DecimalField(max_digits=16, decimal_places=2)
    delivery_insurance_price = models.DecimalField(max_digits=16, decimal_places=2)
    delivery_total_price = models.DecimalField(max_digits=16, decimal_places=2)
    delivery_pickup_order_date = models.DateTimeField(auto_created=True)
    delivery_pickup_date = models.DateTimeField(auto_created=True)
    delivery_est_date = models.DateTimeField(auto_created=True)
    delivery_actual_date = models.DateTimeField(auto_created=True)
    delivery_status = models.CharField(max_length=50, null=True)
    delivery_tracking_number = models.CharField(max_length=100, null=True)
    delivery_ref_number = models.CharField(max_length=100, null=True)
    delivery_origin_branch = models.CharField(max_length=100, null=True)
    delivery_destination_branch = models.CharField(max_length=100, null=True)
    delivery_tlc_branch_code = models.CharField(max_length=100, null=True)
    delivery_label = models.CharField(max_length=500, null=True)
    delivery_tracking_url = models.CharField(max_length=255, null=True)
    delivery_notes = models.CharField(max_length=100, null=True)
    delivery_address = models.CharField(max_length=255, null=True)
    delivery_postal_code = models.CharField(max_length=10, null=True)
    delivery_city = models.CharField(max_length=100, null=True)
    delivery_state = models.CharField(max_length=100, null=True)
    delivery_phone_number = models.CharField(max_length=50, null=True)
    delivery_email = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Gold Transaction {self.order_delivery_id} - Type:"
