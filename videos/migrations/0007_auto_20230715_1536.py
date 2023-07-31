# Generated by Django 2.2.16 on 2023-07-15 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20230715_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubevideo',
            name='youtube_video_duration',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='youtubevideo',
            name='youtube_video_published_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='youtubevideo',
            name='youtube_video_start_time',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]