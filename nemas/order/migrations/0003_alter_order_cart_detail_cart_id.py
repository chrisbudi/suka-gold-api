# Generated by Django 4.2.8 on 2025-02-19 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_order_tracking_order_shipping_order_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_cart_detail',
            name='cart_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='order.order_cart'),
        ),
    ]
