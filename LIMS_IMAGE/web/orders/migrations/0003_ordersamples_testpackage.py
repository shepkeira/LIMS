# Generated by Django 3.2.8 on 2021-11-02 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0001_initial'),
        ('orders', '0002_ordertest_test_id'),
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
            name='OrderSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratory.sample')),
            ],
        ),
    ]
