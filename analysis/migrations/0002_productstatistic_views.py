# Generated by Django 3.0.7 on 2020-06-19 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productstatistic',
            name='views',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]