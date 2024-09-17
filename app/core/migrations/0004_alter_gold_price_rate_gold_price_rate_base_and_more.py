# Generated by Django 4.2.8 on 2024-09-17 01:41

from django.db import migrations, models
import django_ulid.models
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_gold_price_rate_gold_price_rate_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gold_price_rate',
            name='gold_price_rate_base',
            field=models.DecimalField(decimal_places=2, max_digits=18),
        ),
        migrations.AlterField(
            model_name='gold_price_rate',
            name='gold_price_rate_id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
