# Generated by Django 3.0.7 on 2020-06-19 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0003_auto_20200619_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productstatistic',
            name='product',
        ),
        migrations.AddField(
            model_name='productstatistic',
            name='url',
            field=models.CharField(default='', max_length=240, unique=True),
            preserve_default=False,
        ),
    ]
