# Generated by Django 3.2.11 on 2022-01-29 05:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('laboratoryOrders', '0002_ordertest_testpackage'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sample',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
