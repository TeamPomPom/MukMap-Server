# Generated by Django 2.2.16 on 2022-04-10 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceclicklog',
            name='deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='devicesearchlog',
            name='deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
