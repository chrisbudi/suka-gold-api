# Generated by Django 4.2.8 on 2025-02-26 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_delivery_partner_district_city_name_and_more'),
        ('order', '0010_remove_order_gold_order_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_gold',
            old_name='order_postal_code',
            new_name='order_payment_method',
        ),
        migrations.RenameField(
            model_name='order_payment',
            old_name='order_gold_id',
            new_name='order_gold',
        ),
        migrations.RemoveField(
            model_name='order_gold',
            name='order_post_code',
        ),
        migrations.AddField(
            model_name='order_gold',
            name='order_admin_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_gold',
            name='order_tracking_insurance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_gold',
            name='order_tracking_insurance_admin',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_gold',
            name='order_tracking_packing',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_gold',
            name='order_tracking_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_gold_detail',
            name='order_weight',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order_gold_detail',
            name='cert_price_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.gold_cert_price'),
        ),
        migrations.AlterField(
            model_name='order_gold_detail',
            name='gold_price_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.gold_price_config'),
        ),
        migrations.AlterField(
            model_name='order_gold_detail',
            name='gold_type',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
