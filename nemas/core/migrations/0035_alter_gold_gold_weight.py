# Generated by Django 4.2.8 on 2025-03-19 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_alter_gold_product_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gold',
            name='gold_weight',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]
