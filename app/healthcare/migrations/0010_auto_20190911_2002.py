# Generated by Django 2.2.4 on 2019-09-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0009_auto_20190911_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consellingquestionsetsanswers',
            name='question_set',
        ),
        migrations.AddField(
            model_name='patientconsellingquestionresult',
            name='result',
            field=models.ManyToManyField(to='healthcare.ConsellingQuestionSetsAnswers'),
        ),
    ]
