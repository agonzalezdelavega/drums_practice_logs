# Generated by Django 4.2.2 on 2023-08-16 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0017_alter_exercise_source_alter_session_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='days_since_last_practice',
            field=models.IntegerField(default=0),
        ),
    ]
