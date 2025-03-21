# Generated by Django 4.2.8 on 2025-02-03 16:33

import core.fields.uuidv7_field
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid6


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_bank_bank_create_code_va_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='topup_transaction',
            fields=[
                ('topup_transaction_id', core.fields.uuidv7_field.UUIDv7Field(default=uuid6.uuid7, editable=False, primary_key=True, serialize=False, unique=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('topup_payment_method', models.CharField(max_length=255)),
                ('topup_timestamp', models.DateTimeField(auto_now_add=True)),
                ('topup_amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('topup_total_amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('topup_admin', models.DecimalField(decimal_places=2, max_digits=16)),
                ('topup_payment_bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('topup_payment_number', models.CharField(max_length=255)),
                ('topup_payment_ref', models.CharField(max_length=255)),
                ('topup_payment_ref_code', models.CharField(max_length=255)),
                ('topup_payment_channel_code', models.CharField(blank=True, max_length=40, null=True)),
                ('topup_payment_expires_at', models.DateTimeField(auto_now_add=True)),
                ('topup_notes', models.TextField(default='')),
                ('topup_status', models.CharField(default='PENDING', max_length=255)),
                ('update_user', models.CharField(max_length=255)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('update_user_id', models.CharField(max_length=255)),
                ('topup_payment_bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.bank')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
