# Generated by Django 3.2.12 on 2022-02-10 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratoryOrders', '0006_alter_inspection_sample'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inspection',
            old_name='valid',
            new_name='inspection_results',
        ),
        migrations.AddField(
            model_name='inspection',
            name='material_integrity',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inspection',
            name='package_integrity',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
