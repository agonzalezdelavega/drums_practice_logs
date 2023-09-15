from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Session, Exercise, Source, Goal
from django.db.models import Min, Max
from datetime import datetime as dt, timedelta

@receiver(post_save, sender=Session)
def update_dslp_on_save(sender, instance, **kwargs):
    user_sessions = Session.objects.filter(user=instance.user)
   
    previous_dates = user_sessions.order_by("date").filter(date__lt=instance.date).values()
    if previous_dates.count() > 0:
        latest_session_date = previous_dates[previous_dates.count()-1]['date']
        new_dslp = (instance.date - latest_session_date).days
        user_sessions.filter(date=instance.date).update(days_since_last_practice=new_dslp)
    proceeding_dates = user_sessions.order_by("date").filter(date__gt=instance.date).values()
    if proceeding_dates.count() > 0:
        next_session_date = proceeding_dates[0]['date']
        new_dslp = (next_session_date - instance.date).days
        user_sessions.filter(date=next_session_date).update(days_since_last_practice=new_dslp)

@receiver(pre_delete, sender=Session)
def update_dslp_on_delete(sender, instance, **kwargs):
    user_sessions = Session.objects.filter(user=instance.user)
    
    if user_sessions.aggregate(Min('date'))['date__min'] == instance.date:
        proceeding_session = user_sessions.order_by('date').filter(date__gte=instance.date)[0]
        new_dslp = 0
        user_sessions.filter(date=proceeding_session.date).update(days_since_last_practice=new_dslp)
    elif user_sessions.exclude(id=instance.id).filter(date=instance.date).count() == 0 and user_sessions.aggregate(Max("date"))["date__max"] != instance.date:
        preceeding_session = user_sessions.order_by('-date').filter(date__lt=instance.date)[0]
        proceeding_session = user_sessions.order_by('date').filter(date__gt=instance.date)[0]
        new_dslp = (proceeding_session.date - preceeding_session.date).days
        user_sessions.filter(date=proceeding_session.date).update(days_since_last_practice=new_dslp)

# Update progress on goal after saving a new session
@receiver(post_save, sender=Session)
def update_goals_on_save(sender, instance, **kwargs):
    user = instance.user
    exercise = instance.exercise
    user_goals = Goal.objects.filter(user=user)
    
    for goal in user_goals:
        # Check if progress applies to current period
        # 1. Get dates for current period
        match goal.period:
            case "Weekly":
                check_start_date = max(instance.date - timedelta(days=7), goal.start_date)
            case "Biweekly":
                check_start_date = max(instance.date - timedelta(days=14), goal.start_date)
            case "Monthly":
                check_start_date = max(instance.date - timedelta(days=30), goal.start_date)
        # 2. Check how many times this exercise has been practiced for the past period
        # 2a. Use the appropriate filters if no exercise was defined for the user's goal
        if goal.exercise == None:
            session_count = Session.objects.filter(user=user, date__range=[check_start_date, goal.end_date]).count()
        else:
            session_count = Session.objects.filter(user=user, date__range=[check_start_date, goal.end_date], exercise=exercise).count()
        # 3. If the goal has not been met yet for the current period, add it to the user's progress
        if session_count < goal.frequency:
            goal.progress += 1
            goal.save()
    
@receiver(pre_delete, sender=Session)
def update_goals_on_delete(sender, instance, **kwargs):
    user = instance.user
    exercise = instance.exercise
    user_goals = Goal.objects.filter(user=user, exercise_id__in=[exercise, None])
    
    for goal in user_goals:
        # Check if progress applies to current period
        # 1. Get dates for current period
        match goal.period:
            case "weekly":
                check_start_date = max(instance.date - timedelta(days=7), instance.start_date)
            case "biweekly":
                check_start_date = max(instance.date - timedelta(days=14), instance.start_date)
            case "monthly":
                check_start_date = max(instance.date - timedelta(days=30), instance.start_date)
        # 2. Check how many times this exercise has been practiced for the past period
        # 2a. Use the appropriate filters if no exercise was defined for the user's goal
        if goal.exercise == None:
            session_count = Session.objects.filter(user=user, date__in=[check_start_date, goal.end_date]).count()
        else:
            session_count = Session.objects.filter(user=user, date__in=[check_start_date, goal.end_date], exercise=exercise).count()
        # 3. If the goal has not been met yet for the current period, add it to the user's progress
        if session_count < instance.frequency:
            goal.progress -= 1
            goal.save()