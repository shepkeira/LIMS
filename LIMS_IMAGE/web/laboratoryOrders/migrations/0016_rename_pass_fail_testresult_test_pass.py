# Generated by Django 3.2.12 on 2022-03-01 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laboratoryOrders', '0015_alter_testresult_result'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testresult',
            old_name='pass_fail',
            new_name='test_pass',
        ),
    ]
