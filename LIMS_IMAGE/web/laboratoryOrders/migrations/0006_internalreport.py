# Generated by Django 3.2.12 on 2022-02-16 00:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('laboratoryOrders', '0005_alter_sampleinspection_inspector'),
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
    ]
