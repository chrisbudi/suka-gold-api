# Generated by Django 4.2.8 on 2025-03-19 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0027_rename_user_id_order_cart_detail_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_cart',
            old_name='user_id',
            new_name='user',
        ),
    ]
