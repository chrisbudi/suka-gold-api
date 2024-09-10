from django.db import models
from app.core.models.gold import gold

# Create your models here.
# buy, sell, buyback, sellback, transfer
class gold_transaction(models.Model):
    
    def __str__(self):
        return f"Gold Transaction {self.gold_transaction_id} - Type: {self.type}"
    
    
class gold_transfer(models.Model):
    def __str__(self):
        return f"Gold Transfer {self.gold_transfer_id} - Type: {self.type}";

class gold_buy(models.Model):

    def __str__(self):
        return f"Gold Buy {self.gold_buy_id} - Type: {self.type}";

class user_gold_history(models.Model):
    def __str__(self):
        return f"User Gold History {self.user_gold_history_id} - Type: {self.type}";

    
