# Generated by Django 2.2.4 on 2019-10-20 00:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0029_auto_20191020_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientlabtest',
            name='requested_delivery_date',
        ),
        migrations.AddField(
            model_name='patientlabtest',
            name='requested_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 20, 0, 29, 50, 989477)),
            preserve_default=False,
        ),
    ]
