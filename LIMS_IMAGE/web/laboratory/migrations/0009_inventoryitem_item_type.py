# Generated by Django 3.2.12 on 2022-02-11 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0008_alter_inventoryitem_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryitem',
            name='item_type',
            field=models.CharField(choices=[('Solvent', 'Solvent'), ('Organic', 'Organic'), ('Liquid', 'Liquid'), ('Inorganic', 'Inorganic'), ('Standard', 'Standard')], default='Solvent', max_length=10),
        ),
    ]
