# Generated by Django 3.2.12 on 2022-02-18 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0008_alter_test_name'),
        ('orders', '0008_auto_20220218_1406'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('laboratoryOrders', '0006_auto_20220216_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternalReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('type', models.CharField(choices=[('lab', 'Lab Report'), ('operations', 'Operations Report')], max_length=100)),
                ('approved', models.BooleanField()),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lab', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='laboratory.location')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laboratoryOrders.internalreport')),
            ],
        ),
    ]
