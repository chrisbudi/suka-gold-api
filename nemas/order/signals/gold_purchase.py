from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from core.domain import gold_price

from user.models import user_gold_history, user_wallet_history, user_props
from django.db import transaction

User = get_user_model()


# @receiver(post_save, sender=gold_saving_buy)
# def handle_order(
#     sender: type[gold_saving_buy], instance: gold_saving_buy, created, **kwargs
# ):
#     print(created, "created", "gold saving buy")
#     if created:
#         with transaction.atomic():
#             # update user props
#             user_props_instance: user_props = user_props.objects.get(user=instance.user)
#             user_props_instance.gold_wgt += instance.weight
#             user_props_instance.wallet_amt -= instance.price
#             user_props_instance.save()

#             price = gold_price().get_active_price()
#             if price is None:
#                 raise ValueError("Active gold price not found")

#             user_gold_history.objects.create(
#                 user=instance.user,
#                 gold_purchase_date=datetime.now(),
#                 gold_weight=instance.weight,
#                 gold_history_price_base=price.gold_price_base,
#                 gold_history_price_buy=price.gold_price_buy,
#                 gold_history_price_sell=price.gold_price_sell,
#                 gold_history_type="C",
#                 gold_history_amount=0,
#                 gold_history_note="sale-" + str(instance.gold_transaction_id),
#             )

#             user_wallet_history.objects.create(
#                 user=instance.user,
#                 wallet_history_date=datetime.now(),
#                 wallet_history_amount=instance.price,
#                 wallet_history_type="D",
#                 wallet_history_notes="sale-" + str(instance.gold_transaction_id),
#             )
