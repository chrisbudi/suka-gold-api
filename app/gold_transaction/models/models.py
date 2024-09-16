from django.conf import settings

from django.db import models
from core.models.gold import gold
from django_ulid.models import ULIDField, ulid

# Create your models here.
# buy, sell, buyback, sellback, transfer
class gold_transaction(models.Model):
    gold_transaction_id = ULIDField(primary_key=True, unique=True, default=ulid.new, editable=False, max_length=26)
    
    def __str__(self):
        return f"Gold Transaction {self.gold_transaction_id} - Type: {self.type}"
    
    
class gold_transfer(models.Model):
    gold_transfer_id = ULIDField(primary_key=True, unique=True, default=ulid.new, editable=False, max_length=26)
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gold_transfers_from'
    )
    
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gold_transfers_to'
    )
    transfer_ref_number = models.CharField(max_length=255)
    transfer_member_datetime = models.DateTimeField(auto_created=True)
    transfer_member_gold_weight = models.DecimalField(max_digits=8, decimal_places=4)
    transfer_member_notes = models.TextField()
    def __str__(self):
        return f"Gold Transfer {self.gold_transfer_id} - Type: {self.type}";

class gold_buy(models.Model):
    gold_buy_id = ULIDField(primary_key=True, unique=True, default=ulid.new, editable=False, max_length=26)

    def __str__(self):
        return f"Gold Buy {self.gold_buy_id} - Type: {self.type}";

class user_gold_history(models.Model):
    gold_buy_id = ULIDField(primary_key=True, unique=True, default=ulid.new, editable=False, max_length=26)

    def __str__(self):
        return f"User Gold History {self.user_gold_history_id} - Type: {self.type}";

    
