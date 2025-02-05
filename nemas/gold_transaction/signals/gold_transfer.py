from django.db.models.signals import post_save
from django.dispatch import receiver
from gold_transaction.models import gold_transfer
from user.models import user_gold_history
from core.domain import gold_price
from datetime import datetime
from decimal import Decimal


@receiver(post_save, sender=gold_transfer)
def handle_transfer(sender, instance: gold_transfer, created: bool, **kwargs):
    if created:
        # update user props
        user_props = instance.user_from.user_props
        user_props.gold_wgt -= instance.transfer_member_gold_weight
        user_props.save()

        to_user_props = instance.user_to.user_props
        to_user_props.gold_wgt += instance.transfer_member_gold_weight
        to_user_props.save()

        price_instance = gold_price()
        price = price_instance.get_active_price()
        if price is None:
            raise ValueError("Active gold price not found")

        user_gold_history.objects.bulk_create(
            [
                user_gold_history(
                    user=instance.user_from,
                    gold_purchase_date=datetime.now(),
                    gold_weight=instance.transfer_member_gold_weight,
                    gold_history_price_base=price.gold_price_base,
                    gold_history_price_buy=price.gold_price_buy,
                    gold_history_price_sell=price.gold_price_sell,
                    gold_history_type="C",
                    gold_history_amount=0,
                    gold_history_note="transfer-" + instance.transfer_ref_number,
                ),
                user_gold_history(
                    user=instance.user_to,
                    gold_purchase_date=datetime.now(),
                    gold_weight=instance.transfer_member_gold_weight,
                    gold_history_price_base=price.gold_price_base,
                    gold_history_price_buy=price.gold_price_buy,
                    gold_history_price_sell=price.gold_price_sell,
                    gold_history_type="D",
                    gold_history_amount=0,
                    gold_history_note="transfer-" + instance.transfer_ref_number,
                ),
            ]
        )
