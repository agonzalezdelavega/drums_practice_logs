from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime as dt, timedelta
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
    exercises = models.ManyToManyField(Exercise, through="SessionExercise")
    days_since_last_practice = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class SessionExercise(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    bpm = models.PositiveIntegerField()
    
class Goal(models.Model):
    PERIODS = [
        ("Weekly", "Weekly"),
        ("Biweekly", "Biweekly"),
        ("Monthly", "Monthly"),
    ]
    
    STATUS = [
        ("complete", "Completed"),
        ("in_progress", "In Progress"),
        ("expired", "Expired")
    ]
    
    date_validation_msg = "End date must be between a week and a month after the start date"
    
    start_date = models.DateField(auto_now_add=False, default=dt.today)
    end_date = models.DateField(auto_now_add=False, default=dt.today)
    frequency = models.IntegerField(default=1)
    period = models.CharField(choices=PERIODS, max_length=8)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_DEFAULT, default="", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    progress = models.DecimalField(max_digits=5, decimal_places=4, default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    status = models.CharField(choices=STATUS, max_length=11, default="in_progress")
    
    def clean(self):
        start_date = self.start_date
        end_date = self.end_date
        if not end_date >= start_date + timedelta(days=7):
            raise ValidationError("End date must be at least 1 week after start date")
        elif end_date > start_date + timedelta(days=31):
            raise ValidationError("End date cannot be more than 1 month after start date")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
