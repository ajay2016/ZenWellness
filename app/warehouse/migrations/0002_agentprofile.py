# Generated by Django 2.2.4 on 2019-09-03 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import warehouse.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_delete_agentprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('location', '0001_initial'),
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(max_length=255)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to=warehouse.models.user_directory_path)),
                ('remark', models.TextField(blank=True, null=True)),
                ('designation', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Designation')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='location.Location')),
                ('permanent_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permanent_address', to='location.Location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ManyToManyField(to='warehouse.WareHouse')),
            ],
        ),
    ]