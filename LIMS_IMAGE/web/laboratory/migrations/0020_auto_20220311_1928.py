# Generated by Django 3.2.12 on 2022-03-12 03:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0019_auto_20220311_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='cost_per_unit',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='last_ordered',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 11, 19, 28, 50, 557082)),
        ),
        migrations.AlterField(
            model_name='inventoryitem',
            name='total_value',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]