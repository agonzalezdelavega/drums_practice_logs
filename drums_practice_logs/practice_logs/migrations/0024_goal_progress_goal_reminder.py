# Generated by Django 4.2.2 on 2023-09-13 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0023_alter_goal_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='progress',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='goal',
            name='reminder',
            field=models.BooleanField(default=False),
        ),
    ]
