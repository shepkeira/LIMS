# Generated by Django 3.2.12 on 2022-02-03 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0005_test_sample_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='uploads/images')),
            ],
        ),
    ]
