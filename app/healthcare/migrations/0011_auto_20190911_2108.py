# Generated by Django 2.2.4 on 2019-09-11 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0010_auto_20190911_2002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consellingquestionsetsanswers',
            name='answer',
        ),
        migrations.AddField(
            model_name='consellingquestionsetsanswers',
            name='answer_choice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='healthcare.QuestionChoices'),
        ),
        migrations.AddField(
            model_name='consellingquestionsetsanswers',
            name='answer_description',
            field=models.TextField(null=True),
        ),
    ]
