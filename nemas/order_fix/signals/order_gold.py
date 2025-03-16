from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from core.domain import gold_price

from user.models import user_gold_history, user_wallet_history, user_props
from django.db import transaction
from order.models import order_gold

User = get_user_model()


@receiver(post_save, sender=order_gold)
def handle_order(sender: type[order_gold], instance: order_gold, created, **kwargs):
    print(created, "created", "gold saving buy")
    if created:
        # send email send grid service
        pass
