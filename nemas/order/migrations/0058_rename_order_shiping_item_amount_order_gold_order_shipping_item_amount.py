# Generated by Django 4.2.8 on 2025-05-07 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0057_order_gold_order_shiping_item_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_gold',
            old_name='order_shiping_item_amount',
            new_name='order_shipping_item_amount',
        ),
    ]
