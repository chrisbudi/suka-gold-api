# Generated by Django 4.2.8 on 2025-02-03 16:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0038_alter_user_reset_token_expires_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_reset_token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 2, 4, 16, 28, 18, 903744, tzinfo=datetime.timezone.utc)),
        ),
    ]
