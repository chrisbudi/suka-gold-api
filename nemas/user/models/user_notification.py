from django.conf import settings

from django.db import models
from core.fields.uuidv7_field import UUIDv7Field


# Create your models here.
# buy, sell, buyback, sellback, transfer


# create enum for transaction types
class NotificationTransactionType(models.TextChoices):
    GOLD_BUY = "gold_buy", "Buy"
    GOLD_SELL = "gold_sell", "Sell"
    GOLD_TRANSFER_SEND = "gold_transfer_send", "Transfer Send"
    GOLD_TRANSFER_RECEIVE = "gold_transfer_receive", "Transfer Receive"
    ORDER_GOLD = "order_gold", "Order Gold"
    TARIK_EMAS = "tarik_emas", "Tarik Emas"
    TOPUP = (
        "topup",
        "Top Up",
    )
    WITHDRAW = "withdraw", "Withdraw"
    FORGOT_PASSWORD = "forgot_password", "Forgot Password"
    EMAIL_VERIFICATION = "email_verification", "Email Verification"


# create enum for icon types
class NotificationIconType(models.TextChoices):
    INFO = "info", "Info"
    TRANSACTION = "transaction", "Transaction"


class user_notification(models.Model):
    user_notification_id = UUIDv7Field(primary_key=True, unique=True, editable=False)
    user_notification_title = models.CharField(max_length=1000, blank=True, null=True)
    user_notification_description = models.TextField(blank=True, null=True)
    user_notification_date = models.DateTimeField(auto_now_add=True)
    user_notification_icon_type = models.CharField(
        max_length=100, default="info", choices=NotificationIconType.choices
    )
    user_transaction_type = models.CharField(
        max_length=100,
        choices=NotificationTransactionType.choices,
        blank=True,
        null=True,
    )
    user_transaction_id = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
