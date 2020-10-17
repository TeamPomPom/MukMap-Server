# Generated by Django 2.2.16 on 2020-10-17 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('device_token', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'device',
            },
        ),
    ]
