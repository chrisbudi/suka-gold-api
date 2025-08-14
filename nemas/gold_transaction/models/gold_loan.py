from decimal import Decimal
from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field


class gold_loan(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    gold_sell_number = models.CharField(max_length=100, blank=True, null=True)
    gold_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    price = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal(0))
    gold_history_price_base = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    gold_history_price_sell = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    total_price = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    transaction_date = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Completed"
    )

    def __str__(self):
        return f"Gold Transaction {self.gold_transaction_id} - Type:"

    def update_status(self, status: str):
        self.status = status
        self.save()


# Create your models here.
# buy, sell, buyback, sellback, transfer
class gold_saving_buy(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    gold_transaction_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    gold_buy_number = models.CharField(max_length=100, blank=True, null=True)
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=4,
    )
    price = models.DecimalField(max_digits=16, decimal_places=2, default=Decimal(0))
    gold_history_price_base = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    gold_history_price_buy = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )

    total_price = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    transaction_date = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Completed"
    )

    def __str__(self):
        return f"Gold Transaction {self.gold_transaction_id} - Type:"

    def update_status(self, status: str):
        self.status = status
        self.save()


class gold_transfer(models.Model):
    gold_transfer_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    gold_transfer_number = models.CharField(max_length=100, blank=True, null=True)
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gold_transfers_from",
    )
    phone_number = models.CharField(max_length=255, blank=False, null=False)
    user_from_name = models.CharField(max_length=255)
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="gold_transfers_to",
    )
    user_to_name = models.CharField(max_length=255)
    transfer_ref_number = models.CharField(max_length=255)
    transfer_member_datetime = models.DateTimeField(auto_created=True)
    transfer_member_gold_weight = models.DecimalField(max_digits=8, decimal_places=4)
    transfer_member_transfered_weight = models.DecimalField(
        max_digits=8, decimal_places=4, default=Decimal(0)
    )
    transfer_member_admin_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal(0)
    )
    transfer_member_admin_weight = models.DecimalField(
        max_digits=8, decimal_places=4, default=Decimal(0)
    )
    transfer_member_admin_amount = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    transfer_member_amount_received = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    transfer_member_notes = models.TextField()
    transfer_member_service_option = models.CharField(
        max_length=100, blank=True, null=True
    )
    gold_history_price_sell = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )
    gold_history_price_buy = models.DecimalField(
        max_digits=16, decimal_places=2, default=Decimal(0)
    )

    def get_transfer_cost(self, weight: float):
        weight_cost = 0.0
        if weight <= 10:
            weight_cost = 0.001 * weight
            if weight_cost < 0.0001:
                weight_cost = 0.0001

        elif weight > 10 and weight <= 50:
            weight_cost = 0.0008 * weight
        elif weight > 50:
            weight_cost = 0.0003 * weight
        return weight_cost

    def get_transfer_cost_percentage(self, weight: float):
        percentage = 0.0
        if weight <= 10:
            percentage = 0.1
        elif weight > 10 and weight <= 50:
            percentage = 0.08
        elif weight > 50:
            percentage = 0.03
        return percentage

    def send_notification(self, user_from, user_to):

        from shared.utils.notification import (
            NotificationTransactionType,
            NotificationIconType,
            create_user_notification,
        )

        create_user_notification(
            user=user_from,
            icon_type=NotificationIconType.TRANSACTION,
            title="Gold Transfer Sent",
            message=f"You have sent {self.transfer_member_gold_weight} grams of gold to {user_to.name}.",
            transaction_type=NotificationTransactionType.GOLD_TRANSFER_SEND,
        )

        create_user_notification(
            user=user_to,
            icon_type=NotificationIconType.TRANSACTION,
            title="Gold Transfer Received",
            message=f"You have received {self.transfer_member_gold_weight} grams of gold from {user_from.name}.",
            transaction_type=NotificationTransactionType.GOLD_TRANSFER_RECEIVE,
        )

    def __str__(self):
        return f"Gold Transfer {self.gold_transfer_id} - Type:"
