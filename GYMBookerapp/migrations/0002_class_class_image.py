# Generated by Django 4.2.1 on 2023-05-13 11:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GYMBookerapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='class_image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='class_images/'),
            preserve_default=False,
        ),
    ]
