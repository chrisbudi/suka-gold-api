# Generated by Django 4.2.8 on 2025-03-19 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0026_order_cart_detail_product_cost'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_cart_detail',
            old_name='user_id',
            new_name='user',
        ),
    ]
