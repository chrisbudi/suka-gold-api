# Generated by Django 4.2.8 on 2025-05-03 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0052_order_shipping_delivery_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_shipping',
            name='delivery_destination_branch',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order_shipping',
            name='delivery_label',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='order_shipping',
            name='delivery_origin_branch',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order_shipping',
            name='delivery_ref_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order_shipping',
            name='delivery_tlc_branch_code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
