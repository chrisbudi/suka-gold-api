# Generated by Django 4.2.8 on 2025-02-27 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_alter_order_gold_tracking_last_updated_datetime_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_gold_detail',
            old_name='order_gold_id',
            new_name='order_gold',
        ),
    ]
