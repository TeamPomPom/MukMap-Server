# Generated by Django 2.2.16 on 2020-11-17 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201115_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfavoriterestaurant',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite_restaurants', to='restaurants.Restaurants'),
        ),
        migrations.AlterField(
            model_name='userfavoriterestaurant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorite_restaurants', to=settings.AUTH_USER_MODEL),
        ),
    ]
