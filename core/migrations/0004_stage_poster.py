# Generated by Django 5.2 on 2025-04-04 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_log_rating_log_status_log_times'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to='posters/'),
        ),
    ]
