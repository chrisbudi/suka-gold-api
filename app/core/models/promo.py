
from django.db import models

# Promotion Information Model

class InformationPromo(models.Model):
    id_promo = models.AutoField(primary_key=True)
    promo_code = models.CharField(max_length=255)  # kode untuk dapat promo
    leveling_user = models.CharField(max_length=50)  # all level, silver, gold, platinum
    promo_name = models.CharField(max_length=255)
    promo_url = models.CharField(max_length=255)
    promo_start_date = models.DateTimeField()
    promo_end_date = models.DateTimeField()
    promo_tag = models.CharField(max_length=255)  # SHARE
    promo_url_background = models.CharField(max_length=255)
    promo_diskon = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # Optional
    promo_cashback = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)  # Optional
    promo_cashback_tipe_user = models.CharField(max_length=255, blank=True, null=True)  # Optional
    merchant_cashback = models.CharField(max_length=255, blank=True, null=True)  # Optional
    createtime = models.DateTimeField(auto_now_add=True)
    createuser = models.CharField(max_length=255)
    updtime = models.DateTimeField(auto_now=True)
    upduser = models.CharField(max_length=255)

    def __str__(self):
        return self.promo_name
