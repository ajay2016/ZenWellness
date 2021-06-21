# Generated by Django 2.2.4 on 2019-09-11 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0006_patientprofile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientconsellingquestionresult',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='healthcare.DoctorProfile'),
        ),
        migrations.AlterField(
            model_name='patientconsellingquestionresult',
            name='finding',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='patientconsellingquestionresult',
            name='recommendation',
            field=models.TextField(blank=True, null=True),
        ),
    ]