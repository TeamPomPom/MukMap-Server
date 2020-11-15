# Generated by Django 2.2.16 on 2020-11-15 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('station_name', models.CharField(max_length=150)),
                ('full_address', models.CharField(max_length=500)),
                ('lat', models.DecimalField(decimal_places=7, max_digits=20)),
                ('lng', models.DecimalField(decimal_places=7, max_digits=20)),
                ('line', models.CharField(max_length=40)),
                ('alias', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'subway',
            },
        ),
    ]
