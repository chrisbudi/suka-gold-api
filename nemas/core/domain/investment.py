from django.db import models


class AdminFee(models.Model):
    """
    Master data for admin fees applicable on investments.
    """

    FEE_TYPE_CHOICES = [
        ("percentage", "Percentage"),
        ("fixed", "Fixed Amount"),
    ]
    name = models.CharField(max_length=100, unique=True)
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    value = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Percentage or fixed amount"
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.fee_type} - {self.value})"


class InvestmentReturn(models.Model):
    """
    Master data for defining ROI schemes or rates.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="ROI rate as a percentage (e.g., 5.00 for 5%)",
    )
    duration_days = models.PositiveIntegerField(
        help_text="Duration for ROI calculation in days"
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.rate}% for {self.duration_days} days"
