# Generated by Django 4.2.8 on 2025-06-23 08:57

import core.fields.uuidv7_field
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid6


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0067_user_notification_user_transaction_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_notification_price',
            fields=[
                ('user_notification_price_id', core.fields.uuidv7_field.UUIDv7Field(default=uuid6.uuid7, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user_notification_price_max', models.DecimalField(decimal_places=2, max_digits=16)),
                ('user_notification_price_min', models.DecimalField(decimal_places=2, max_digits=16)),
                ('timestamps', models.DateTimeField(auto_now_add=True)),
                ('user_notification_price_status', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
