# Generated by Django 3.2.9 on 2021-11-22 05:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='account_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]