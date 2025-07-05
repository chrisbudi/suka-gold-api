from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from core.domain import payment_method


class order_payment(models.Model):
    order_payment_bill_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    order_gold = models.ForeignKey(
        "order_gold",
        on_delete=models.CASCADE,
    )
    order_payment_timestamp = models.DateTimeField(auto_created=True)
    order_payment_amount = models.DecimalField(max_digits=16, decimal_places=2)
    order_payment_summary_amount = models.DecimalField(max_digits=16, decimal_places=2)
    order_payment_summary_amount_round = models.DecimalField(
        max_digits=16, decimal_places=0
    )
    order_payment_admin_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_payment_method = models.ForeignKey(
        payment_method,
        on_delete=models.CASCADE,
    )
    order_payment_method_name = models.CharField(max_length=50, null=True)
    order_payment_va_bank = models.CharField(max_length=30, null=True)
    order_payment_va_number = models.CharField(max_length=50, null=True)
    order_payment_number = models.CharField(max_length=2000)
    order_payment_ref = models.CharField(max_length=255)
    order_payment_status = models.CharField(max_length=255)

    def __str__(self):
        return f"Gold Transaction {self.order_payment_bill_id} - Type:"
