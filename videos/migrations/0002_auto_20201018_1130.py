# Generated by Django 2.2.16 on 2020-10-18 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtubevideosubcategory',
            old_name='video',
            new_name='youtube_video',
        ),
    ]