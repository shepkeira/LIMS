# Generated by Django 3.2.12 on 2022-03-12 03:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0016_auto_20220311_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='cost_per_unit',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='last_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 11, 19, 21, 48, 545466)),
        ),
    ]
