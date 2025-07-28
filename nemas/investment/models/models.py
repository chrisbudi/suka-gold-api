from django.db import models
from django.contrib.auth import get_user_model


from core.domain import InvestmentReturn
from core.fields.uuidv7_field import UUIDv7Field


class TransactionModel(models.Model):
    """
    Records transactions for investments including fee and return calculations.
    """

    transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    User = get_user_model()
    investor = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(max_digits=15, decimal_places=2)
    weight_invested = models.DecimalField(max_digits=10, decimal_places=4, blank=True)

    date_invested = models.DateField(auto_now_add=True)

    investment_return = models.ForeignKey(InvestmentReturn, on_delete=models.PROTECT)
    investment_weight_return = models.DecimalField(
        max_digits=10, decimal_places=4, blank=True
    )

    return_amount = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True
    )

    date_returned = models.DateField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        # Calculate ROI return amount if returned
        if self.is_returned and self.investment_return:
            # Simple calculation based on invested amount and ROI rate
            self.return_amount = (
                self.amount_invested * self.investment_return.rate
            ) / 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Investment by {self.investor.username} on {self.date_invested} - Amount: {self.amount_invested}"
