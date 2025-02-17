from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from datetime import datetime
from core.domain import gold_price

from wallet.models import disburst_transaction
from user.models import user_gold_history, user_wallet_history, user_props
from django.db import transaction

User = get_user_model()


@receiver(post_save, sender=disburst_transaction)
def handle_disburst(
    sender: type[disburst_transaction],
    instance: disburst_transaction,
    created,
    **kwargs
):
    print(created, "created", "gold saving buy")
    if created:
        with transaction.atomic():
            # update user props
            user_props_instance: user_props = user_props.objects.get(user=instance.user)
            user_props_instance.wallet_amt -= instance.disburst_total_amount
            user_props_instance.save()

            user_wallet_history.objects.create(
                user=instance.user,
                wallet_history_date=datetime.now(),
                wallet_history_amount=instance.disburst_total_amount,
                wallet_history_type="D",
                wallet_history_notes="disb-" + str(instance.disburst_transaction_id),
            )
