# Generated by Django 4.2.8 on 2024-09-17 02:51

from django.db import migrations
import django_ulid.models
import ulid.api.api


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_id_alter_user_props_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='user_props',
            name='id',
            field=django_ulid.models.ULIDField(default=ulid.api.api.Api.new, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
