# Generated by Django 3.2.12 on 2022-03-14 23:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0020_auto_20220311_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='last_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 14, 16, 28, 23, 165810)),
        ),
    ]
