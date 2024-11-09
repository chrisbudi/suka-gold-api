# from taggit.managers import TaggableManager
from django.db import models


class order_promo(models.Model):
    order_promo_id = models.AutoField(primary_key=True)
    order_promo_code = models.CharField(max_length=50)
    order_promo_description = models.CharField(max_length=255)

    # amt promo
    order_promo_weight = models.DecimalField(max_digits=8, decimal_places=4)
    order_promo_amt_pct = models.DecimalField(max_digits=10, decimal_places=2)
    order_promo_amt = models.DecimalField(max_digits=10, decimal_places=2)

    # promo requirement
    order_promo_min_weight = models.DecimalField(max_digits=8, decimal_places=4)
    order_promo_max_weight = models.DecimalField(max_digits=8, decimal_places=4)
    order_promo_min_amt = models.DecimalField(max_digits=10, decimal_places=2)
    order_promo_max_amt = models.DecimalField(max_digits=10, decimal_places=2)

    # promo date
    order_promo_start_date = models.DateField()
    order_promo_end_date = models.DateField()

    order_promo_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=255)
    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.CharField(max_length=255)

    def __str__(self):
        return f"GPC {self.order_promo_id} - Weight: {self.order_promo_description}"
