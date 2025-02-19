# Generated by Django 4.2.8 on 2025-02-18 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_bank_bank_create_code_va_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='delivery_partner',
            fields=[
                ('delivery_partner_id', models.AutoField(primary_key=True, serialize=False)),
                ('delivery_partner_name', models.CharField(max_length=50, unique=True)),
                ('delivery_partner_description', models.CharField(max_length=50, unique=True)),
            ],
        ),
    ]
