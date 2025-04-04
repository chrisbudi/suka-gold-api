from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from core.domain import gold_price

from django.db import transaction
from order.models import order_gold, order_cart, order_cart_detail

User = get_user_model()


@receiver(post_save, sender=order_gold)
def handle_order_gold(
    sender: type[order_gold], instance: order_gold, created, **kwargs
):
    # update order cart to complete true
    with transaction.atomic():
        if instance.order_cart is not None:
            order_cart_model = order_cart.objects.get(
                order_cart_id=instance.order_cart.order_cart_id
            )
        else:
            raise ValueError("instance.order_cart is None, cannot access order_cart_id")
        order_cart_model.completed_cart = True
        order_cart_model.save()

        order_cart_detail_model = order_cart_detail.objects.filter(
            cart_id=instance.order_cart.order_cart_id
        )

        for detail in order_cart_detail_model:
            detail.completed_cart = True
            detail.save()

    print(created, "created", "gold saving buy")

    if created:
        # send email send grid service
        pass
