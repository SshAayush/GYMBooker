# Generated by Django 4.1.3 on 2023-04-28 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GYMBookerapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_resetcode',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_login_history',
            field=models.DateTimeField(),
        ),
    ]
