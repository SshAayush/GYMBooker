# Generated by Django 4.2.1 on 2023-10-02 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GYMBookerapp', '0008_alter_customer_customer_currheight_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='customer_startbmi',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
