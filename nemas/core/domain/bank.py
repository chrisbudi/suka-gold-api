from django.db import models
import random


class bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_code = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=255, unique=True)
    bank_merchant_code = models.CharField(max_length=10, unique=True)
    bank_logo_url = models.CharField(max_length=255, blank=True, null=True)
    bank_active = models.BooleanField(default=True)

    bank_closed_va_code = models.CharField(max_length=50, blank=True, null=True)
    bank_open_va_code = models.CharField(max_length=50, blank=True, null=True)
    bank_va_range_start = models.CharField(max_length=50, blank=True, null=True)
    bank_va_range_end = models.CharField(max_length=50, blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=255)
    upd_time = models.DateTimeField(auto_now=True)
    upd_user = models.CharField(max_length=255)

    class Meta:
        app_label = "core"

    def __str__(self):
        return f"bank id {self.bank_id} - bank name: {self.bank_name}"

    def generate_va(self) -> str:
        # generate value from range bank_va_range_start and bank_va_range_end
        if self.bank_va_range_start and self.bank_va_range_end:
            start = int(self.bank_va_range_start)
            end = int(self.bank_va_range_end)
            if start <= end:
                return str(random.randint(start, end))
            else:
                raise ValueError("Invalid VA range: start is greater than end")
        else:
            raise ValueError("VA range start or end is not defined")
