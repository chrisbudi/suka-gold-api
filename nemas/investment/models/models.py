from django.db import models
from django.contrib.auth import get_user_model


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


class InvestmentTransaction(models.Model):
    """
    Records transactions for investments including fee and return calculations.
    """

    User = get_user_model()
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    date_invested = models.DateField(auto_now_add=True)

    admin_fee = models.ForeignKey(AdminFee, on_delete=models.PROTECT)
    fee_amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )

    investment_return = models.ForeignKey(InvestmentReturn, on_delete=models.PROTECT)
    return_amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )

    date_returned = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Calculate fee amount
        if self.admin_fee:
            if self.admin_fee.fee_type == "percentage":
                self.fee_amount = (self.amount_invested * self.admin_fee.value) / 100
            else:
                self.fee_amount = self.admin_fee.value

        # Calculate ROI return amount if returned
        if self.is_returned and self.investment_return:
            # Simple calculation based on invested amount and ROI rate
            self.return_amount = (
                self.amount_invested * self.investment_return.rate
            ) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Investment by {self.investor.username} on {self.date_invested} - Amount: {self.amount_invested}"
