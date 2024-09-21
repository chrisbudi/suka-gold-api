from django.db import models
from django_ulid.models import ULIDField, ulid


class gold_price_config(models.Model):
    gpc_id = models.AutoField(primary_key=True)
    gpc_code = models.CharField(max_length=50) # 
    gold_price_weight = models.IntegerField()
    gold_price_setting_model = models.TextField()
    
    gpc_active = models.BooleanField(default=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createuser = models.CharField(max_length=255)
    updtime = models.DateTimeField(auto_now=True)
    upduser = models.CharField(max_length=255)

    def __str__(self):
        return f"GPC {self.gpc_id} - Weight: {self.gold_price_weight}"

