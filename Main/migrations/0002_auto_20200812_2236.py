# Generated by Django 3.0.7 on 2020-08-12 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bots',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
