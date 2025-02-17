from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from core.domain import gold


class order_cart(models.Model):
    order_cart_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f"Gold Transaction {self.order_cart_id} - Type:"


class order_cart_detail(models.Model):
    order_gold_detail_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    cart_id = models.ForeignKey(
        order_cart,
        on_delete=models.CASCADE,
    )
    gold_id = models.ForeignKey(
        gold,
        on_delete=models.CASCADE,
    )
    quantitiy = models.IntegerField()
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)

    class Meta:
        unique_together = ["cart_id", "gold_id"]
