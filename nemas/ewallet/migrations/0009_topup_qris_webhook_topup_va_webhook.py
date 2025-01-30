# Generated by Django 4.2.8 on 2025-01-30 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ewallet', '0008_topup_transaction_topup_payment_bank_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='topup_qris_webhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(max_length=50)),
                ('payment_id', models.CharField(max_length=255, unique=True)),
                ('business_id', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], max_length=20)),
                ('qr_id', models.CharField(max_length=255)),
                ('reference_id', models.CharField(max_length=255)),
                ('channel_code', models.CharField(max_length=50)),
                ('expires_at', models.DateTimeField()),
                ('metadata', models.JSONField(default=dict)),
                ('payment_detail', models.JSONField(default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('raw_data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='topup_va_webhook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=255, unique=True)),
                ('account_number', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('external_id', models.CharField(max_length=255)),
                ('bank_code', models.CharField(max_length=50)),
                ('transaction_time', models.DateTimeField(null=True)),
                ('raw_data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
