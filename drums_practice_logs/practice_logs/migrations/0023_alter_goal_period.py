# Generated by Django 4.2.2 on 2023-09-13 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0022_goal_period_alter_goal_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='period',
            field=models.CharField(choices=[('Weekly', 'Weekly'), ('Biweekly', 'Biweekly'), ('Monthly', 'Monthly')], max_length=8),
        ),
    ]