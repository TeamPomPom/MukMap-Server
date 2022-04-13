# Generated by Django 2.2.16 on 2022-04-13 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0005_auto_20220410_1430'),
        ('restaurants', '0002_auto_20220410_1430'),
        ('devices', '0003_auto_20220410_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceSubscribeChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_subscribe_channels', to='devices.Device')),
                ('youtube_channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_subscribe_channels', to='channels.YoutubeChannel')),
            ],
            options={
                'db_table': 'device_subscribe_channel',
            },
        ),
        migrations.CreateModel(
            name='DeviceFavoriteRestaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_favorite_restaurants', to='devices.Device')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_favorite_restaurants', to='restaurants.Restaurants')),
            ],
            options={
                'db_table': 'device_favorite',
            },
        ),
        migrations.AddField(
            model_name='device',
            name='favorite',
            field=models.ManyToManyField(related_name='devices', through='devices.DeviceFavoriteRestaurant', to='restaurants.Restaurants'),
        ),
        migrations.AddField(
            model_name='device',
            name='subscribe',
            field=models.ManyToManyField(related_name='devices', through='devices.DeviceSubscribeChannel', to='channels.YoutubeChannel'),
        ),
    ]