# Generated by Django 2.2.4 on 2019-09-04 07:48

from django.db import migrations, models
import django.db.models.deletion
import warehouse.models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_agentprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agentprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=warehouse.models.agent_directory_path),
        ),
        migrations.AlterField(
            model_name='producttransaction',
            name='warehouse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='warehouse.WareHouse'),
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='products',
        ),
        migrations.AddField(
            model_name='warehouse',
            name='products',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='warehouse.Product'),
            preserve_default=False,
        ),
    ]