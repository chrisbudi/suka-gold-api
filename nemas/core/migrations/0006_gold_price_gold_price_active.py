# Generated by Django 4.2.8 on 2024-12-15 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_order_promo_gold_promo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold_price',
            name='gold_price_active',
            field=models.BooleanField(default=True),
        ),
    ]
