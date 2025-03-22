# Generated by Django 4.2.8 on 2025-03-22 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_payment_method'),
        ('order', '0032_alter_order_gold_order_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_payment',
            name='order_payment_admin_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_payment',
            name='order_payment_method',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.payment_method'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_payment',
            name='order_payment_va_bank',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='order_payment',
            name='order_payment_va_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='order_gold',
            name='order_payment_va_bank',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='order_gold',
            name='order_payment_va_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
