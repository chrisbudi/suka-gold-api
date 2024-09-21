# Generated by Django 4.2.8 on 2024-09-17 16:08

from django.db import migrations, models
import django_ulid.models
import ulid.api.api


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='gold_buy',
            fields=[
                ('gold_buy_id', django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='gold_transaction',
            fields=[
                ('gold_transaction_id', django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='gold_transfer',
            fields=[
                ('transfer_member_datetime', models.DateTimeField(auto_created=True)),
                ('gold_transfer_id', django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False, unique=True)),
                ('transfer_ref_number', models.CharField(max_length=255)),
                ('transfer_member_gold_weight', models.DecimalField(decimal_places=4, max_digits=8)),
                ('transfer_member_notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='user_gold_history',
            fields=[
                ('gold_buy_id', django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
