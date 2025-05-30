# Generated by Django 4.2.8 on 2025-02-08 12:53

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0047_alter_user_reset_token_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_reset_token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 9, 12, 53, 8, 26627, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='user_reset_token',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
