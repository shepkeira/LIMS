# Generated by Django 3.2.12 on 2022-02-25 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratoryOrders', '0012_alter_internalreport_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='pass_fail',
            field=models.BooleanField(null=True),
        ),
    ]