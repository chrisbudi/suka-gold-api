from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import transaction
from order.models import (
    order_gold,
    order_cart,
    order_cart_detail,
    order_payment,
)


@receiver(post_save, sender=order_gold)
def handle_order_gold(
    sender: type[order_gold], instance: order_gold, created, **kwargs
):

    order_gold_model: order_gold = instance

    # update order cart to complete true
    if created:
        with transaction.atomic():
            if instance.order_cart is not None:
                order_cart_model = order_cart.objects.get(
                    order_cart_id=instance.order_cart.order_cart_id
                )
            else:
                raise ValueError(
                    "instance.order_cart is None, cannot access order_cart_id"
                )
            order_cart_model.completed_cart = True
            order_cart_model.save()

            order_cart_detail_model = order_cart_detail.objects.filter(
                cart_id=instance.order_cart.order_cart_id
            )

            for detail in order_cart_detail_model:
                detail.completed_cart = True
                detail.save()

        print(created, "created", "gold saving buy")

    else:
        with transaction.atomic():
            if instance.order_gold_payment_status == "PAID":
                order_payment_instance = order_payment.objects.filter(
                    order_gold=instance.order_gold_id
                ).first()
                if order_payment_instance:
                    order_payment_instance.order_payment_status = "PAID"
                    order_payment_instance.save()
