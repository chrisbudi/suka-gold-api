from operator import truediv
from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from core.domain import gold
from django.utils import timezone
from django.contrib.auth import get_user_model


class order_cart(models.Model):
    order_cart_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    cart_status = models.CharField(max_length=50)
    total_weight = models.DecimalField(max_digits=10, decimal_places=4)
    total_price = models.DecimalField(max_digits=16, decimal_places=2)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f"Gold Transaction {self.order_cart_id} - Type:"


class order_cart_detail(models.Model):
    order_cart_detail_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    cart_id = models.ForeignKey(
        order_cart,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    gold_id = models.ForeignKey(
        gold,
        on_delete=models.CASCADE,
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    weight = models.DecimalField(max_digits=10, decimal_places=4)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        unique_together = ["cart_id", "gold_id"]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        if not self.user_id:
            self.user_id = get_user_model().objects.get(pk=self.user_id)

        super().save(*args, **kwargs)
