# Generated by Django 4.2.8 on 2025-01-25 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewallet', '0004_topup_transaction_topup_total_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topup_transaction',
            name='topup_timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
