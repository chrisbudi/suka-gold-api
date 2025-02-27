# Generated by Django 4.2.8 on 2025-02-03 17:51

import core.fields.uuidv7_field
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid6


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gold_transaction', '0007_rename_purchase_date_gold_transaction_transaction_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='gold_saving_buy',
            fields=[
                ('transaction_date', models.DateTimeField(auto_created=True)),
                ('gold_transaction_id', core.fields.uuidv7_field.UUIDv7Field(default=uuid6.uuid7, editable=False, primary_key=True, serialize=False, unique=True)),
                ('weight', models.DecimalField(decimal_places=4, max_digits=8)),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16)),
                ('gold_history_price_base', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16)),
                ('gold_history_price_buy', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16)),
                ('total_price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Completed', max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='gold_saving_sell',
            fields=[
                ('transaction_date', models.DateTimeField(auto_created=True)),
                ('gold_transaction_id', core.fields.uuidv7_field.UUIDv7Field(default=uuid6.uuid7, editable=False, primary_key=True, serialize=False, unique=True)),
                ('weight', models.DecimalField(decimal_places=4, max_digits=8)),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16)),
                ('gold_history_price_base', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16)),
                ('gold_history_price_sell', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16)),
                ('total_price', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=16)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Completed', max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='gold_transaction',
        ),
    ]
