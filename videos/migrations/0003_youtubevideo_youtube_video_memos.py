# Generated by Django 2.2.16 on 2020-10-18 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20201018_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='youtube_video_memos',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
