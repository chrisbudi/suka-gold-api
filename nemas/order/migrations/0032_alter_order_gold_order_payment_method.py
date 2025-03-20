# Generated by Django 4.2.8 on 2025-03-20 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_payment_method'),
        ('order', '0031_order_gold_tracking_courier_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_gold',
            name='order_payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.payment_method'),
        ),
    ]
