# Generated by Django 2.2.16 on 2022-04-10 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainfoodcategory',
            name='deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subfoodcategory',
            name='deleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
