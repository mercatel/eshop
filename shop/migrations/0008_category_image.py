# Generated by Django 3.0.6 on 2020-06-11 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20200603_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='category'),
            preserve_default=False,
        ),
    ]
