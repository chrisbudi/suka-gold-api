# Generated by Django 4.2.8 on 2025-02-27 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_rename_gold_id_order_cart_detail_gold'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_gold',
            name='order_pickup_address',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
