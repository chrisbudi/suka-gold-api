# Generated by Django 4.2.8 on 2025-01-14 02:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_user_verify_notes_user_verify_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_ktp',
            name='photo_url',
        ),
        migrations.AddField(
            model_name='user',
            name='photo_ktp_url',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='photo_selfie_url',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user_reset_token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 15, 2, 46, 16, 601628, tzinfo=datetime.timezone.utc)),
        ),
    ]
