# Generated by Django 4.2.8 on 2025-05-04 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0062_user_address_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='member_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
