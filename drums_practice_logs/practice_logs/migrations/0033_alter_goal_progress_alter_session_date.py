# Generated by Django 4.2.2 on 2023-10-08 23:01

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0032_remove_session_bpm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='progress',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(default=datetime.datetime.today, validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 10, 8), message='Please choose a day on or before today')]),
        ),
    ]