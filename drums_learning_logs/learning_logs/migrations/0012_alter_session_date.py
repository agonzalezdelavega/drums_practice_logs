# Generated by Django 4.2.2 on 2023-08-02 19:57

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0011_alter_session_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(default=datetime.datetime.today, validators=[django.core.validators.MaxValueValidator(datetime.date(2023, 8, 2), message='Please choose a day on or before <built-in method today of type object at 0x56192d979e20>')]),
        ),
    ]
