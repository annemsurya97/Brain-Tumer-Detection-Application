# Generated by Django 3.2.25 on 2024-09-17 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_data',
            name='time',
            field=models.TimeField(auto_now=True),
        ),
    ]
