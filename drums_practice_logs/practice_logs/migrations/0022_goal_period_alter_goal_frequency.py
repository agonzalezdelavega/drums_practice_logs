# Generated by Django 4.2.2 on 2023-09-13 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0021_alter_goal_end_date_alter_goal_start_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='period',
            field=models.CharField(choices=[('weekly', 'Weekly'), ('biweekly', 'Biweekly'), ('monthly', 'Monthly')], default=None, max_length=8),
        ),
        migrations.AlterField(
            model_name='goal',
            name='frequency',
            field=models.IntegerField(default=1),
        ),
    ]
