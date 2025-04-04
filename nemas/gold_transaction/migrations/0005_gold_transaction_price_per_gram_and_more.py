# Generated by Django 4.2.8 on 2025-01-29 19:07

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gold_transaction', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gold_transaction',
            name='price_per_gram',
            field=models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=8),
        ),
        migrations.AddField(
            model_name='gold_transaction',
            name='purchase_date',
            field=models.DateTimeField(auto_created=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gold_transaction',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Completed', max_length=50),
        ),
        migrations.AddField(
            model_name='gold_transaction',
            name='total_price',
            field=models.DecimalField(decimal_places=4, default=Decimal('0'), max_digits=8),
        ),
        migrations.AddField(
            model_name='gold_transaction',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gold_transaction',
            name='weight',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
