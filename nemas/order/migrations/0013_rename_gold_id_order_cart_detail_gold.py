# Generated by Django 4.2.8 on 2025-02-27 03:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_rename_gold_id_order_gold_detail_gold'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_cart_detail',
            old_name='gold_id',
            new_name='gold',
        ),
    ]
