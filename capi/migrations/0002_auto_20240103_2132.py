# Generated by Django 3.2.3 on 2024-01-03 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capi', '0001_initial'),
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