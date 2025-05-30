# Generated by Django 4.2.8 on 2025-05-08 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0060_order_gold_order_tracking_total_amount_rounded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order_gold',
            name='order_pph22_round',
        ),
        migrations.RemoveField(
            model_name='order_gold',
            name='order_shipping_item_amount',
        ),
        migrations.RemoveField(
            model_name='order_gold',
            name='order_tracking_insurance_round',
        ),
        migrations.AddField(
            model_name='order_gold',
            name='order_tracking_item_insurance_amount',
            field=models.DecimalField(decimal_places=2, max_digits=16, null=True),
        ),
        migrations.AddField(
            model_name='order_gold',
            name='tracking_courier_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order_gold',
            name='tracking_courier_service_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order_gold',
            name='order_pph22',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='order_gold',
            name='order_tracking_insurance_admin',
            field=models.DecimalField(decimal_places=0, max_digits=10, null=True),
        ),
    ]
