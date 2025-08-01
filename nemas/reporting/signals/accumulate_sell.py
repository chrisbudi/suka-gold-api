from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import date

from gold_transaction.models import gold_saving_sell
from ..models import daily_summary, monthly_summary
from user.models import user_props
from django.db import transaction


@receiver(post_save, sender=gold_saving_sell)
def accumulate_sell(sender, instance: gold_saving_sell, created, **kwargs):
    if not created:
        return

    user = instance.user
    amount = instance.price
    today = now().date()
    month = today.replace(day=1)

    @transaction.atomic
    def update():
        daily, _ = daily_summary.objects.get_or_create(user=user, summary_date=today)
        daily.total_sell += amount
        daily.save(update_fields=["total_sell", "updated_at"])

        monthly, _ = monthly_summary.objects.get_or_create(
            user=user, summary_month=month
        )
        monthly.total_sell += amount
        monthly.save(update_fields=["total_sell", "updated_at"])

        prop = user_props.objects.get(user=user)
        prop.total_sell += amount
        prop.save(update_fields=["total_sell", "update_time"])
        prop.update_level()

    update()
