# Generated by Django 4.2.8 on 2025-01-11 09:17

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_reset_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_reset_token',
            name='id',
        ),
        migrations.AlterField(
            model_name='user_reset_token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 12, 9, 17, 47, 620533, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='user_reset_token',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
