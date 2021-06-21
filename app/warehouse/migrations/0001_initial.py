# Generated by Django 2.2.4 on 2019-09-01 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import warehouse.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=warehouse.models.user_directory_path)),
                ('remark', models.TextField(blank=True, null=True)),
                ('is_online_product', models.BooleanField(default=True)),
                ('include_in_prescription', models.BooleanField(default=True)),
                ('required_prescription', models.BooleanField(default=True)),
                ('composition', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'In-Active')], default='A', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'In-Active')], default='A', max_length=2)),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.SubDiscipline')),
                ('products', models.ManyToManyField(to='warehouse.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('I', 'Stock In'), ('O', 'Stock Out')], max_length=1)),
                ('rate', models.DecimalField(decimal_places=4, max_digits=15)),
                ('quantity', models.IntegerField()),
                ('discount', models.DecimalField(blank=True, decimal_places=4, max_digits=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.MedicineBrand')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.MedicineCompany')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.WareHouse')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('A', 'Active'), ('I', 'In-Active')], default='A', max_length=2)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='warehouse.ProductCategory')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_subcategory', to='warehouse.ProductSubCategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='discipline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.SubDiscipline'),
        ),
    ]