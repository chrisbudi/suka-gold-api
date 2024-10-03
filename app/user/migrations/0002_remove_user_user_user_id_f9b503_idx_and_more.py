# Generated by Django 4.2.8 on 2024-10-03 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='user',
            name='user_user_id_f9b503_idx',
        ),
        migrations.RenameField(
            model_name='user_ktp',
            old_name='ktp_create_time',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='user_ktp',
            old_name='ktp_create_user',
            new_name='create_user',
        ),
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['id', 'email', 'user_name'], name='user_user_id_5c826d_idx'),
        ),
    ]
