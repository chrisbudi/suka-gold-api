# Generated by Django 4.2.8 on 2024-09-21 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gold',
            old_name='createtime',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='gold',
            old_name='createuser',
            new_name='create_user',
        ),
        migrations.RenameField(
            model_name='gold',
            old_name='updtime',
            new_name='upd_time',
        ),
        migrations.RenameField(
            model_name='gold',
            old_name='upduser',
            new_name='upd_user',
        ),
        migrations.RenameField(
            model_name='gold_cert_price',
            old_name='createtime',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='gold_cert_price',
            old_name='createuser',
            new_name='create_user',
        ),
        migrations.RenameField(
            model_name='gold_price_config',
            old_name='createtime',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='gold_price_config',
            old_name='createuser',
            new_name='create_user',
        ),
        migrations.RenameField(
            model_name='gold_price_config',
            old_name='updtime',
            new_name='upd_time',
        ),
        migrations.RenameField(
            model_name='gold_price_config',
            old_name='upduser',
            new_name='upd_user',
        ),
    ]
