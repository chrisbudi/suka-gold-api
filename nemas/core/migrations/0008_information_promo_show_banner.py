# Generated by Django 4.2.8 on 2024-12-28 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='information_promo',
            name='show_banner',
            field=models.BooleanField(default=True),
        ),
    ]
