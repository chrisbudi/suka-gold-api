# Generated by Django 4.2.8 on 2025-05-20 15:19

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gold_transaction', '0018_gold_transfer_transfer_member_admin_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gold_transfer',
            name='transfer_member_admin_price',
        ),
        migrations.AddField(
            model_name='gold_transfer',
            name='transfer_member_transfered_weight',
            field=models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=8),
        ),
    ]
