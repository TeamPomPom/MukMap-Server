# Generated by Django 2.2.16 on 2020-11-17 14:43

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0003_youtubechannel_channel_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youtubechannel',
            name='channel_country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]