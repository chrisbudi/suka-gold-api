from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from core.domain import gold_price

from django.db import transaction
from order.models import order_gold
from order.models import order_payment

User = get_user_model()


@receiver(post_save, sender=order_payment)
def handle_order_gold_payment(
    sender: type[order_payment], instance: order_payment, created, **kwargs
):
    # update order payment summary to latest
    with transaction.atomic():
        order_gold_model: order_gold = instance.order_gold
        order_gold_model.order_gold_payment_status = instance.order_payment_status
        if (
            order_gold_model.order_gold_payment_status == "ISSUED"
            or not order_gold_model.order_gold_payment_ref
        ):
            order_gold_model.order_gold_payment_ref = instance.order_payment_ref
    if created:
        # send email send grid service
        pass
