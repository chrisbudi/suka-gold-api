# from taggit.managers import TaggableManager
from django.db import models
from requests import delete


class gold_promo(models.Model):
    gold_promo_id = models.AutoField(primary_key=True)
    gold_promo_code = models.CharField(max_length=50)
    gold_promo_description = models.CharField(max_length=255)

    # amt promo
    gold_promo_weight = models.DecimalField(max_digits=8, decimal_places=4)
    gold_promo_amt_pct = models.DecimalField(max_digits=10, decimal_places=2)
    gold_promo_amt = models.DecimalField(max_digits=10, decimal_places=2)

    # promo requirement
    gold_promo_min_weight = models.DecimalField(max_digits=8, decimal_places=4)
    gold_promo_max_weight = models.DecimalField(max_digits=8, decimal_places=4)
    gold_promo_min_amt = models.DecimalField(max_digits=10, decimal_places=2)
    gold_promo_max_amt = models.DecimalField(max_digits=10, decimal_places=2)

    # promo date
    gold_promo_start_date = models.DateField()
    gold_promo_end_date = models.DateField()

    gold_promo_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.UUIDField(null=True)
    create_user_mail = models.CharField(max_length=255, null=True)
    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.UUIDField(null=True)
    upd_user_mail = models.CharField(max_length=255, null=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"GPC {self.gold_promo_id} - Weight: {self.gold_promo_description}"

    def delete(self):
        self.is_deleted = True
        self.save()
