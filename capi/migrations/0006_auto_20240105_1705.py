# Generated by Django 3.2.3 on 2024-01-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capi', '0005_auto_20240105_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='id',
        ),
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]