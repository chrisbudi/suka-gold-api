from django.conf import settings

from django.db import models
from core.domain.gold import gold
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer
class topup_transaction(models.Model):
    topup_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    topup_timestamp = models.DateTimeField(auto_created=True)
    topup_amount = models.DecimalField(max_digits=16, decimal_places=2)
    topup_admin = models.DecimalField(max_digits=16, decimal_places=2)
    topup_payment_method = models.CharField(max_length=255)
    topup_payment_number = models.CharField(max_length=255)
    topup_payment_bank = models.CharField(max_length=255)
    topup_payment_ref = models.CharField(max_length=255)
    topup_notes = models.TextField()
    topup_status = models.CharField(max_length=255)
    create_user = models.CharField(max_length=255)
    update_user_id = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    update_user = models.CharField(max_length=255)
    update_date = models.DateTimeField(auto_now=True)
    update_user_id = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            if not self.pk:
                self.create_user = user.username
                self.create_user_id = user.id
            self.update_user = user.username
            self.update_user_id = user.id
        super().save(*args, **kwargs)

    class Meta:
        app_label = "ewallet"

    def __str__(self):
        return f"TOPUP Transaction {self.topup_transaction_id} - Type:"
