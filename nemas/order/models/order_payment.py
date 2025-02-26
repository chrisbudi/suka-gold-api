from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from order.models import order_gold


class order_payment(models.Model):
    order_payment_bill_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_gold = models.ForeignKey(
        "order_gold",
        on_delete=models.CASCADE,
    )
    order_payment_timestamp = models.DateTimeField(auto_created=True)
    order_payment_amount = models.DecimalField(max_digits=16, decimal_places=2)
    order_payment_external_id = models.CharField(max_length=255)
    order_payment_number = models.CharField(max_length=255)
    order_payment_ref = models.CharField(max_length=255)
    order_payment_status = models.CharField(max_length=255)

    def __str__(self):
        return f"Gold Transaction {self.order_payment_bill_id} - Type:"
