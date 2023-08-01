from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime as dt


class Source(models.Model):
    SOURCE_TYPES = [
        ("book", "Book"),
        ("online_platform", "Online Platform"),
        ("online_article", "Online Article"),
        ("video_guide", "Video Guide"),
        ("other", "Other")
    ]
    
    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(choices=SOURCE_TYPES, max_length=15)
    author = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    source = models.ForeignKey(Source, on_delete=models.PROTECT, blank=True, null=True)
    page = models.IntegerField(default=1, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    times_practiced = models.IntegerField(default=0)
    percent_completed = models.DecimalField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)], max_digits=3, decimal_places=2)

    def __str__(self):
        return self.name

class Session(models.Model):
    date = models.DateField(auto_now_add=False, default=dt.today)
    time_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, blank=True, null=True)
    bpm = models.IntegerField()
    days_since_last_practice = models.IntegerField(default=1)