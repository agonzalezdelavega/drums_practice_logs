from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime as dt
from django.contrib.auth.models import User


class Source(models.Model):
    SOURCE_TYPES = [
        ("book", "Book"),
        ("online_platform", "Online Platform"),
        ("online_article", "Online Article"),
        ("video_guide", "Video Guide"),
        ("other", "Other")
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(choices=SOURCE_TYPES, max_length=15)
    author = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [["name", "user"]]

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    page = models.IntegerField(default=1, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    times_practiced = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        unique_together = [["name", "source"]]

class Session(models.Model):
    date = models.DateField(auto_now_add=False, default=dt.today, 
                            validators=[MaxValueValidator(dt.today().date(), message=f"Please choose a day on or before today")])
    time_minutes = models.IntegerField(validators=[MinValueValidator(1)])
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    bpm = models.IntegerField()
    days_since_last_practice = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Goal(models.Model):
    PERIODS = [
        ("Weekly", "Weekly"),
        ("Biweekly", "Biweekly"),
        ("Monthly", "Monthly"),
    ]
    
    start_date = models.DateField(auto_now_add=False, default=dt.today)
                            # validators=[MinValueValidator(dt.today().date(), message=f"Please choose a day on or after today")])
    end_date = models.DateField(auto_now_add=False, default=dt.today)
                            # validators=[MinValueValidator(dt.today().date(), message=f"Please choose a day on or after today")])
    frequency = models.IntegerField(default=1)
    period = models.CharField(choices=PERIODS, max_length=8)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_DEFAULT, default="", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    reminder = models.BooleanField(default=False)
    
    @property
    def progress_percent(self):
        return int(self.progress / self.frequency * 100)