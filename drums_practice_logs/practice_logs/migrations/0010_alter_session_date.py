# Generated by Django 4.2.2 on 2023-08-02 19:45

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0009_alter_exercise_source_alter_session_exercise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(default=datetime.datetime.today, validators=[django.core.validators.MaxValueValidator(datetime.datetime.today, message='Please choose a day on or before <built-in method today of type object at 0x55837d977e20>')]),
        ),
    ]