# Generated by Django 4.2.8 on 2025-02-27 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_order_gold_order_payment_va_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_gold',
            name='tracking_last_updated_datetime',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
        migrations.AlterField(
            model_name='order_gold',
            name='tracking_sla',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]
