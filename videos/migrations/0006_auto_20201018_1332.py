# Generated by Django 2.2.16 on 2020-10-18 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_auto_20201018_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubevideo',
            name='youtube_video_duration',
            field=models.IntegerField(default=0),
        ),
    ]
