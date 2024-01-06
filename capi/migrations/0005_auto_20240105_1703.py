from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('capi', '0004_alter_video_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='file',
            field=models.TextField(default=''),
        ),
    ]
