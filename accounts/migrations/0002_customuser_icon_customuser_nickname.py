# Generated by Django 5.2 on 2025-04-10 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons/'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
