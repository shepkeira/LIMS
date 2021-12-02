# Generated by Django 3.2.9 on 2021-12-01 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0004_auto_20211130_2357'),
        ('orders', '0006_auto_20211201_0012'),
        ('laboratoryOrders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.package')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratory.test')),
            ],
        ),
        migrations.CreateModel(
            name='OrderTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('test_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratory.test')),
            ],
        ),
    ]
