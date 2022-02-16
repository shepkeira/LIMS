# Generated by Django 3.2.12 on 2022-02-11 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0007_remove_image_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='status',
            field=models.CharField(choices=[('Ordered', 'Ordered'), ('Received', 'Received'), ('Shipped', 'Shipped'), ('Arrived', 'Arrived'), ('Completed', 'Completed')], default='Ordered', max_length=10),
        ),
    ]