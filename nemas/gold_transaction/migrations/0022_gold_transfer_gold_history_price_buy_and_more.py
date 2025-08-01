# Generated by Django 4.2.8 on 2025-07-08 12:18

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gold_transaction', '0021_gold_transfer_transfer_member_admin_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold_transfer',
            name='gold_history_price_buy',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16),
        ),
        migrations.AddField(
            model_name='gold_transfer',
            name='gold_history_price_sell',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16),
        ),
    ]
