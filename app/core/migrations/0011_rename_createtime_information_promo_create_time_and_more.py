# Generated by Django 4.2.8 on 2024-11-09 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_order_promo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='information_promo',
            old_name='createtime',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='information_promo',
            old_name='createuser',
            new_name='create_user',
        ),
        migrations.RenameField(
            model_name='information_promo',
            old_name='updtime',
            new_name='upd_time',
        ),
        migrations.RenameField(
            model_name='information_promo',
            old_name='upduser',
            new_name='upd_user',
        ),
    ]
