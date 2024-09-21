"""
Model for golds
"""

from django.db import models
from django_ulid.models import ULIDField, ulid

# Gold Models

class gold_cert_price(models.Model):
    cert_id = models.AutoField(primary_key=True)
    gold_weight = models.IntegerField()
    cert_price = models.DecimalField(max_digits=10, decimal_places=2)
    createtime = models.DateTimeField(auto_now_add=True)
    createuser = models.CharField(max_length=255)

class gold(models.Model):
    gold_id = models.AutoField(primary_key=True)
    gold_weight = models.IntegerField()
    type = models.CharField(max_length=50)  # bar-mintedbar
    brand = models.CharField(max_length=255)  # marva gold, antam
    certificate_number = models.CharField(max_length=255)
    createtime = models.DateTimeField(auto_now_add=True)
    createuser = models.CharField(max_length=255)
    updtime = models.DateTimeField(auto_now=True)
    upduser = models.CharField(max_length=255)
    
    from django.db import models

# Gold Price Setting Model
class gold_price_setting(models.Model):
    gps_id = models.AutoField(primary_key=True)
    weekend_price_buy = models.DecimalField(max_digits=8, decimal_places=2)  # +cost beli user sabtu minggu
    weekend_price_sell = models.DecimalField(max_digits=8, decimal_places=2)  # - harga jual user sabtu minggu
    weekday_price_sell = models.DecimalField(max_digits=8, decimal_places=2)  # - harga jual user hari biasa
    weekday_price_buy_add_cost1 = models.DecimalField(max_digits=8, decimal_places=2)  # + variabel cost1 beli hr biasa
    weekday_price_buy_add_cost2 = models.DecimalField(max_digits=8, decimal_places=2)  # + variabel cost2 beli hr biasa
    weekday_price_buy_add_cost3 = models.DecimalField(max_digits=8, decimal_places=2)  # + variabel cost3 beli hr biasa
    status = models.CharField(max_length=50)  # aktif, non aktif
    updtime = models.DateTimeField(auto_now=True)
    upduser = models.CharField(max_length=255)

    def __str__(self):
        return f"GPS {self.gps_id} - Status: {self.status}"

# Gold Price Model
class gold_price(models.Model):
    gold_price_id = ULIDField(primary_key=True, unique=True, default=ulid.new, editable=False, max_length=26)
    gold_price_source = models.CharField(max_length=50, default="")  # sumber harga emas
    gold_price_weight = models.IntegerField(default=1)  # berat emas
    gold_price_base = models.DecimalField(max_digits=10, decimal_places=2)  # harga dasar emas dr api
    gold_price_sell = models.DecimalField(max_digits=10, decimal_places=2)  # harga dasar + goldpricesetting_sel
    gold_price_buy = models.DecimalField(max_digits=10, decimal_places=2)  # harga dasar + goldpricesetting_buy
    timestamps = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gold Price {self.gold_price_id} - Base: {self.gold_price_base}"
