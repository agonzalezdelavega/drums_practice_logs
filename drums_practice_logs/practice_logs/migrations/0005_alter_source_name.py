# Generated by Django 4.2.2 on 2023-07-31 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice_logs', '0004_alter_exercise_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
