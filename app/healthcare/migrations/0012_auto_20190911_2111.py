# Generated by Django 2.2.4 on 2019-09-11 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0011_auto_20190911_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
