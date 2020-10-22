# Generated by Django 2.2.16 on 2020-10-22 12:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('channel_name', models.CharField(max_length=50)),
                ('channel_thumbnail', models.TextField(blank=True)),
                ('channel_id', models.CharField(max_length=100)),
                ('channel_desc', models.TextField(max_length=10000)),
                ('channel_keyword', models.CharField(blank=True, max_length=500)),
                ('status', models.CharField(choices=[('none_request', 'None request'), ('want_sign_up', 'Want sign up'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='none_request', max_length=30)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='youtube_channels', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'youtube_channel',
            },
        ),
    ]
