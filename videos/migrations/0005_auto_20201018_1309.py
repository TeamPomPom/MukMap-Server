# Generated by Django 2.2.16 on 2020-10-18 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20201018_1308'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youtubevideo',
            old_name='food_main_category',
            new_name='main_food_category',
        ),
        migrations.RenameField(
            model_name='youtubevideo',
            old_name='food_sub_category',
            new_name='sub_food_category',
        ),
    ]
