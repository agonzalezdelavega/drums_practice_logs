from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Session, Exercise, Source, Goal
from django.db.models import Min, Max
from datetime import datetime as dt, timedelta

@receiver(post_save, sender=Session)
def update_dslp_on_save(sender, instance, **kwargs):
    user = instance.exercise.source.user
    user_sources = Source.objects.filter(user=user)
    user_exercises = Exercise.objects.filter(source_id__in=user_sources)
    user_sessions = Session.objects.filter(exercise__in=user_exercises)
    
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
    user = instance.exercise.source.user
    user_sources = Source.objects.filter(user=user)
    user_exercises = Exercise.objects.filter(source_id__in=user_sources)
    user_sessions = Session.objects.filter(exercise__in=user_exercises)
    
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
    user = instance.exercise.source.user
    exercise = instance.exercise
    user_goals = Goal.objects.filter(user=user, exercise_id__in=[exercise, None])
    
    for goal in user_goals:
        # Check if progress applies to current period
        match goal.period:
            case "weekly":
                check_start_date = max(instance.date - timedelta(days=7), instance.start_date)
            case "biweekly":
                check_start_date = max(instance.date - timedelta(days=14), instance.start_date)
            case "monthly":
                check_start_date = max(instance.date - timedelta(days=30), instance.start_date)
        # Check how many times this exercise has been practiced for the past period
        # If the goal has not been met yet for the current period, add it to the user's progress
        # If the goal is to practice any exercise, add session to the user's progress if the goal has not been met yet for the current period
        if goal.exercise == None:
            
            period_frequency = Session.objects.filter()
        goal.progress += 1
        goal.save()
    
@receiver(pre_delete, sender=Session)
def update_goals_on_delete(sender, instance, **kwargs):
    user = instance.exercise.source.user
    exercise = instance.exercise
    user_goals = Goal.objects.filter(user=user, exercise_id__in=[exercise, None])
    
    for goal in user_goals:
        goal.progress -= 1
        goal.save()