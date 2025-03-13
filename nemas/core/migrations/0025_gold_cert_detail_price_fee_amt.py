# Generated by Django 4.2.8 on 2025-03-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_delete_gold_cert_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold_cert_detail_price',
            name='fee_amt',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
            preserve_default=False,
        ),
    ]
