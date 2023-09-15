# Generated by Django 4.2.2 on 2023-09-14 02:02

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0024_goal_progress_goal_reminder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='end_date',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='goal',
            name='start_date',
            field=models.DateField(default=datetime.datetime.today),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(default=datetime.datetime.today, validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 9, 14), message='Please choose a day on or before today')]),
        ),
    ]
