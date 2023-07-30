# from django.db.models.signals import pre_delete, post_save
# from django.dispatch import receiver
# from .models import Session
# from django.db.models import Min

# @receiver(post_save, sender=Session)
# def update_dslp_on_save(sender, instance, **kwargs):
#     previous_dates = Session.objects.order_by("date").filter(date__lt=instance.date).values()
#     if previous_dates.count() > 0:
#         latest_session_date = previous_dates[previous_dates.count()-1]['date']
#         new_dslp = (instance.date - latest_session_date).days
#         Session.objects.filter(date=instance.date).update(days_since_last_practice=new_dslp)
#     proceeding_dates = Session.objects.order_by("date").filter(date__gt=instance.date).values()
#     if proceeding_dates.count() > 0:
#         next_session_date = proceeding_dates[0]['date']
#         new_dslp = (next_session_date - instance.date).days
#         Session.objects.filter(date=next_session_date).update(days_since_last_practice=new_dslp)

# @receiver(pre_delete, sender=Session)
# def update_dslp_on_delete(sender, instance, **kwargs):
#     if Session.objects.aggregate(Min('date'))['date__min'] == instance.date:
#         proceeding_session = Session.objects.order_by('date').filter(date__gt=instance.date)[0]
#         new_dslp = 0
#         Session.objects.filter(date=proceeding_session.date).update(days_since_last_practice=new_dslp)
#     elif Session.objects.exclude(id=instance.id).filter(date=instance.date).count() == 0:
#         preceeding_session = Session.objects.order_by('-date').filter(date__lt=instance.date)[0]
#         proceeding_session = Session.objects.order_by('date').filter(date__gt=instance.date)[0]
#         new_dslp = (proceeding_session.date - preceeding_session.date).days
#         Session.objects.filter(date=proceeding_session.date).update(days_since_last_practice=new_dslp)
