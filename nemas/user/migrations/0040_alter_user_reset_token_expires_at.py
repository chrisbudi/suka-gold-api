# Generated by Django 4.2.8 on 2025-02-03 16:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0039_alter_user_reset_token_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_reset_token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 4, 16, 32, 23, 407770, tzinfo=datetime.timezone.utc)),
        ),
    ]
