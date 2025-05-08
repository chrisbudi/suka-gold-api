from operator import truediv
from click import edit
from django.conf import settings

from django.db import models
from requests import delete
from core.fields.uuidv7_field import UUIDv7Field
from core.domain import gold, cert
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class order_cart(models.Model):
    order_cart_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    total_weight = models.DecimalField(max_digits=10, decimal_places=4)
    total_price = models.DecimalField(max_digits=16, decimal_places=2)
    total_price_round = models.DecimalField(max_digits=16, decimal_places=0)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)
    order_type = models.CharField(max_length=50, null=True, blank=True)
    total_redeem_price = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True
    )

    completed_cart = models.BooleanField(default=False)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    def __uuid__(self):
        return self.order_cart_id

    def remove_cart(self):
        self.completed_cart = True

    def complete_cart(self):
        self.completed_cart = True
        self.save()


class order_cart_detail(models.Model):
    order_cart_detail_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    cart = models.ForeignKey(
        order_cart,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    gold = models.ForeignKey(
        gold,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)]  # Ensures quantity ≥ 1
    )
    cert = models.ForeignKey(
        cert,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    cert_price = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True
    )
    product_cost = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True
    )

    selected = models.BooleanField(default=True)
    weight = models.DecimalField(max_digits=10, decimal_places=4)
    gold_price = models.DecimalField(max_digits=16, decimal_places=2)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    total_price = models.DecimalField(max_digits=16, decimal_places=2, editable=False)
    total_price_round = models.DecimalField(
        max_digits=16, decimal_places=0, editable=False
    )

    order_type = models.CharField(max_length=50, null=True, blank=True)
    redeem_price = models.DecimalField(
        max_digits=16, decimal_places=2, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_created=True)
    completed_cart = models.BooleanField(default=False)

    class Meta:
        unique_together = ["cart", "gold"]

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        if not self.user_id:
            self.user_id = get_user_model().objects.get(pk=self.user_id)
        super().save(*args, **kwargs)

    def complete_cart(self, *args, **kwargs):
        self.completed_cart = True
        self.save()
