from email.policy import default
from operator import is_
from re import I
from django.db import models
from requests import delete
from core.fields.uuidv7_field import UUIDv7Field

from decimal import Decimal as decimal
import random

# Gold Models


class cert(models.Model):
    cert_id = models.AutoField(primary_key=True)
    cert_brand = models.CharField(max_length=255)
    cert_code = models.CharField(max_length=50)
    gold_weight = models.IntegerField()
    cert_price = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_email = models.CharField(max_length=255, null=True)
    upd_user = models.UUIDField(null=True)
    upd_time = models.DateTimeField(auto_now=True)
    upd_user_email = models.CharField(max_length=255, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Cert {self.cert_id} - Name: {self.cert_brand}"

    def delete(self):
        self.is_deleted = True
        self.save()


class gold_cert_detail_price(models.Model):
    id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    gold = models.ForeignKey(
        "gold", on_delete=models.CASCADE, related_name="gold_cert_detail_price"
    )
    gold_cert = models.ForeignKey(cert, on_delete=models.CASCADE)
    gold_cert_code = models.CharField(max_length=50)
    gold_weight = models.IntegerField()
    include_stock = models.BooleanField(default=True)
    fee_amt = models.DecimalField(
        max_digits=16, decimal_places=2, default=decimal("0.00")
    )
    gold_cert_status = models.CharField(max_length=50, default="active")
    create_time = models.DateTimeField(auto_now_add=True)
    create_user_email = models.CharField(max_length=255, null=True)
    create_user = models.UUIDField(null=True)
    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_email = models.CharField(max_length=255, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return str(id)

    def delete(self):
        self.is_deleted = True
        self.save()


class gold(models.Model):
    gold_id = models.AutoField(primary_key=True)
    gold_weight = models.DecimalField(
        max_digits=10,
        decimal_places=4,
    )
    type = models.CharField(max_length=50)  # bar-mintedbar
    brand = models.CharField(max_length=255)  # marva gold, antam
    # TODO: Remove the certificate weight field
    certificate_weight = models.DecimalField(
        max_digits=10, decimal_places=4, default=decimal(0.00)
    )
    certificate = models.ForeignKey(cert, on_delete=models.CASCADE, null=True)
    product_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=decimal(0.00)
    )
    redeem_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=decimal(0.00)
    )  # biaya tarik emas
    gold_image_1 = models.CharField(max_length=255, default="")
    gold_image_2 = models.CharField(max_length=255, default="")
    gold_image_3 = models.CharField(max_length=255, default="")
    gold_image_4 = models.CharField(max_length=255, default="")
    gold_image_5 = models.CharField(max_length=255, default="")
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_email = models.CharField(max_length=255, null=True)
    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_email = models.CharField(max_length=255, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Gold {self.gold_id} - Brand: {self.brand}"

    def generate_number(self):
        return str(random.randint(100000, 999999))

    def get_stock(self):
        return gold_cert_detail_price.objects.filter(
            gold=self, include_stock=True
        ).count()

    def delete(self):
        self.is_deleted = True
        self.save()


# Gold Price Model
class gold_price(models.Model):
    gold_price_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    gold_price_source = models.CharField(max_length=50, default="")  # sumber harga emas
    gold_price_weight = models.IntegerField(default=1)  # berat emas
    gold_price_base = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # harga dasar emas dr api
    gold_price_sell = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # harga dasar + goldpricesetting_sel
    gold_price_buy = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # harga dasar + goldpricesetting_buy
    gold_price_active = models.BooleanField(default=True)
    timestamps = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Gold Price {self.gold_price_id} - Base: {self.gold_price_base}"

    @property
    def gold_price_buy_round(self):
        # Compute rounded value for gold price buy
        return self.gold_price_buy // 100 * 100 + 100

    def get_active_price(self):
        # Example usage of the computed property
        gold_price_model = gold_price.objects.filter(gold_price_active=True).first()
        if not gold_price_model:
            raise ValueError("No active gold price found.")

        return gold_price_model

    def delete(self):
        self.is_deleted = True
        self.save()


class gold_price_source(models.Model):
    gold_price_source_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    gold_price_source = models.CharField(max_length=50, default="")  # sumber harga emas
    gold_price_weight = models.IntegerField(default=1)  # berat emas
    gold_price_base = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # harga dasar emas dr api
    timestamps = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Gold Price Source {self.gold_price_source_id} - Base: {self.gold_price_base}"

    def delete(self):
        self.is_deleted = True
        self.save()
