from django.db import models
from core.fields.uuidv7_field import UUIDv7Field
from django.conf import settings


class user_gold_history(models.Model):
    id = UUIDv7Field(primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="gold_history"
    )
    gold_purchase_date = models.DateTimeField(auto_now_add=True)
    gold_weight = models.DecimalField(max_digits=10, decimal_places=4)
    gold_history_price_base = models.DecimalField(max_digits=10, decimal_places=2)
    gold_history_price_buy = models.DecimalField(max_digits=10, decimal_places=2)
    gold_history_price_sell = models.DecimalField(max_digits=10, decimal_places=2)
    gold_history_type = models.CharField(max_length=1)
    gold_history_amount = models.DecimalField(max_digits=16, decimal_places=2)
    gold_history_note = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user} - {self.gold_purchase_date} - {self.gold_history_amount}"

    def user_gold_history(self, user):
        return self.objects.filter(user=user)

    def user_gold_history_by_date(self, user, start_date, end_date):
        return self.objects.filter(
            user=user, gold_purchase_date__range=[start_date, end_date]
        )

    def user_gold_history_by_type(self, user, gold_history_type):
        return self.objects.filter(user=user, gold_history_type=gold_history_type)


class user_wallet_history(models.Model):
    id = UUIDv7Field(primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wallet_history",
    )
    wallet_history_date = models.DateTimeField(auto_now_add=True)
    wallet_history_amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet_history_type = models.CharField(max_length=1)
    wallet_history_notes = models.CharField(max_length=255)

    def __str__(self):
        return (
            f"{self.user} - {self.wallet_history_date} - {self.wallet_history_amount}"
        )
