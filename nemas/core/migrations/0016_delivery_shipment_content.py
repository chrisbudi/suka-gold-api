# Generated by Django 4.2.8 on 2025-02-22 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_delivery_partner'),
    ]

    operations = [
        migrations.CreateModel(
            name='delivery_shipment_content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_type_code', models.CharField(max_length=50, unique=True)),
                ('shipment_content_code', models.CharField(max_length=50, unique=True)),
                ('shipment_content_name', models.CharField(max_length=100)),
            ],
        ),
    ]
