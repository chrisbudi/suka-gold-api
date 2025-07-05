from decimal import Decimal
from django.db import models

from django.contrib.auth.models import User

from core.fields.uuidv7_field import UUIDv7Field


class daily_user_summary(models.Model):
    daily_user_summary_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    summary_date = models.DateField()
    total_buy = models.DecimalField(
        max_digits=20, decimal_places=4, default=Decimal("0")
    )
    total_sell = models.DecimalField(
        max_digits=20, decimal_places=4, default=Decimal("0")
    )
    latest_buy = models.DecimalField(
        max_digits=20, decimal_places=4, default=Decimal("0")
    )
    latest_sell = models.DecimalField(
        max_digits=20, decimal_places=4, default=Decimal("0")
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "summary_date")
