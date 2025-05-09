# Generated by Django 4.2.8 on 2025-05-07 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0054_order_cart_order_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_cart',
            old_name='total_digital_admin_settlement',
            new_name='order_summary_redeem_price',
        ),
        migrations.RenameField(
            model_name='order_cart_detail',
            old_name='digital_admin_settlement',
            new_name='order_detail_redeem_price',
        ),
        migrations.RemoveField(
            model_name='order_cart',
            name='total_digital_admin_settlement_round',
        ),
        migrations.RemoveField(
            model_name='order_cart_detail',
            name='digital_admin_settlement_round',
        ),
        migrations.AddField(
            model_name='order_cart_detail',
            name='order_total_detail_redeem_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True),
        ),
        migrations.AddField(
            model_name='order_gold',
            name='order_total_redeem_price',
            field=models.DecimalField(decimal_places=2, max_digits=16, null=True),
        ),
        migrations.AddField(
            model_name='order_gold',
            name='order_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order_gold_detail',
            name='order_redeem_price',
            field=models.DecimalField(decimal_places=2, max_digits=16, null=True),
        ),
        migrations.AddField(
            model_name='order_gold_detail',
            name='order_type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
