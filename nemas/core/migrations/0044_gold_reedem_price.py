# Generated by Django 4.2.8 on 2025-05-07 01:31

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_payment_method_payment_method_external'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold',
            name='reedem_price',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10),
        ),
    ]
