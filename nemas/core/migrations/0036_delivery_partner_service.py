# Generated by Django 4.2.8 on 2025-03-19 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_alter_gold_gold_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='delivery_partner_service',
            fields=[
                ('delivery_partner_service_id', models.AutoField(primary_key=True, serialize=False)),
                ('delivery_partner_service_name', models.CharField(max_length=50, unique=True)),
                ('delivery_partner_service_code', models.CharField(max_length=50, unique=True)),
                ('delivery_partner_service_description', models.CharField(max_length=50, unique=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
