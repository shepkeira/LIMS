# Generated by Django 3.2.12 on 2022-02-25 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratoryOrders', '0013_alter_testresult_pass_fail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='status',
            field=models.CharField(choices=[('received', 'Recieved'), ('progress', 'In Progress'), ('completed', 'Completed'), ('incomplete', 'Adverse Event')], max_length=100),
        ),
    ]
