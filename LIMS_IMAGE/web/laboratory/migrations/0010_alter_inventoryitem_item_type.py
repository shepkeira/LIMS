# Generated by Django 3.2.12 on 2022-02-11 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0009_inventoryitem_item_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='item_type',
            field=models.CharField(choices=[('Solvent', 'Chemical - Solvent'), ('Organic', 'Chemical - Organic'), ('Inorganic', 'Chemical - Inorganic'), ('Liquid', 'Liquid'), ('Standard', 'Standard'), ('Consumable', 'Consumable')], default='Solvent', max_length=10),
        ),
    ]