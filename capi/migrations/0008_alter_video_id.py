# Generated by Django 3.2.3 on 2024-01-05 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capi', '0007_auto_20240105_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='id',
            field=models.AutoField(primary_key=True),
        ),
    ]
