from django.db import models


class bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_code = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=255, unique=True)
    bank_merchant_code = models.CharField(max_length=10, unique=True)
    bank_logo_url = models.CharField(max_length=255, blank=True, null=True)
    bank_active = models.BooleanField(default=True)

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=255)
    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.CharField(max_length=255)

    def __str__(self):
        return f"bank id {self.bank_id} - bank name: {self.bank_name}"
