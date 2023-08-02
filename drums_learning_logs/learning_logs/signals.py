from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from .models import Session, Exercise, Source
from django.db.models import Min, Max

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
        proceeding_session = user_sessions.order_by('date').filter(date__gt=instance.date)[0]
        new_dslp = 0
        user_sessions.filter(date=proceeding_session.date).update(days_since_last_practice=new_dslp)
    elif user_sessions.exclude(id=instance.id).filter(date=instance.date).count() == 0 and user_sessions.aggregate(Max("date"))["date__max"] != instance.date:
        preceeding_session = user_sessions.order_by('-date').filter(date__lt=instance.date)[0]
        proceeding_session = user_sessions.order_by('date').filter(date__gt=instance.date)[0]
        new_dslp = (proceeding_session.date - preceeding_session.date).days
        user_sessions.filter(date=proceeding_session.date).update(days_since_last_practice=new_dslp)
        