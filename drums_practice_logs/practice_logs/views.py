from django.shortcuts import render, redirect
from .models import Source, Exercise, Session, Goal
from .forms import SessionForm, DateSearchForm, SourceForm, PrintExerciseForm, OnlineExerciseForm, GoalsForm
from datetime import datetime as dt, date, timedelta
import calendar
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64
from django.contrib.auth.decorators import login_required
from django.http import Http404
import logging
import sys

default_start_date = dt.today() - timedelta(days=30)
default_end_date = dt.today()


logger = logging.getLogger('neo-get-data')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def index(request):
    logger.info('Welcome to the drums practice logs!!!!!')
    return render(request, "practice_logs/index.html")

@login_required
def new_session(request):
    if request.method == "POST":
        form = SessionForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_sessions")
    else:
        form = SessionForm(request.user)
    context = {"form": form}
    return render(request, "practice_logs/new_session.html", context)

@login_required
def view_sessions(request, start_date=default_start_date, end_date=default_end_date):
    # Date Form
    if request.method == "POST":
        form = DateSearchForm(data=request.POST)
        start_date = f"{form.data['start_date']}"
        end_date = f"{form.data['end_date']}"
    else:
        form = DateSearchForm()
    
    # Get fields
    fields = [field.name.replace("_", " ").title() for field in Session._meta.get_fields()[1:]]
    fields[fields.index("Time Minutes")] = "Time (Minutes)"
    fields[fields.index("Bpm")] = "BPM"
    
    sources = Source.objects.filter(user=request.user)
    exercises = Exercise.objects.filter(source__in=sources)
    
    # Session Data
    session_data = Session.objects.filter(date__range=[start_date, end_date], exercise__in=exercises).values('id', 'date', 'time_minutes', 'exercise_id', 'bpm',
                                                                                     'days_since_last_practice').order_by('-date')
    # Get exercise name
    for session in session_data:
            session['exercise'] = exercises.get(id=session['exercise_id']).name
    
    context = {
        "session_data": session_data,
        "fields": fields,
        "form": form
    }
    
    return render(request, "practice_logs/view_sessions.html", context)

@login_required
def edit_session(request, session_id):
    session = Session.objects.get(id=session_id)
    
    exercise = session.exercise
    source = exercise.source
    if source.user != request.user:
        raise Http404
    
    if request.method == "POST":
        form = SessionForm(request.user, instance=session, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_sessions")
    else:
        form = SessionForm(request.user, instance=session)
        
    context = {"form": form, "session": session}
    return render(request, "practice_logs/edit_sessions.html", context)

@login_required
def delete_session(request, session_id):
    session = Session.objects.get(id=session_id)
    exercise = session.exercise
    source = exercise.source
    if source.user != request.user:
        raise Http404
    
    session.delete()
    return redirect("practice_logs:view_sessions")

@login_required
def dashboard(request):
    sources = Source.objects.filter(user=request.user)
    exercises = Exercise.objects.filter(source__in=sources)
    session_data = pd.DataFrame(list(Session.objects.filter(
        date__range=[dt.today() - timedelta(days=30), dt.today()] ,exercise__in=exercises).values()))
    
    # Return empty dashboard if user has no session data available
    if len(session_data) < 2:
        context = {
            'session_data': session_data
        }
        return render(request, "practice_logs/dashboard.html", context)
    
    # Dashboard data             
    curr_month = dt.strftime(dt.today(), "%Y-%m")
    days_of_month = calendar.monthrange(int(curr_month[0:4]),int(curr_month[5:]))[1]
    first_day_of_month = f"{curr_month}-01"
    last_day_of_month = f"{curr_month}-{days_of_month}"

    session_data_monthly = Session.objects.filter(date__range=[first_day_of_month, last_day_of_month], exercise__in=exercises).values()
    days_practiced_curr_month =  len(pd.DataFrame(list(session_data_monthly)).groupby('date', as_index=False)) if len(session_data_monthly) > 0 else 0
    average_practice_time = round(session_data.groupby('date', as_index=False).sum()["time_minutes"].mean())
    avg_days_between_practice = round(session_data.groupby('date', as_index=False).mean()["days_since_last_practice"].mean())
    days_since_last_practice = (date.today() - session_data['date'].max()).days
    
    # Consistency Chart
    consistency = session_data.groupby('date', as_index=False).min()
    
    plt.figure(figsize=(18, 8))
    plt.xlabel('Practice Date', fontsize=20)
    plt.ylabel('Number of Days', fontsize=20)
    plt.title("Days Since Last Practice Session", fontsize=30)
    plt.plot(consistency['date'], consistency['days_since_last_practice'])
    
    consistency_chart = plt.gcf()
    buffer = BytesIO()
    consistency_chart.savefig(buffer, format="png")
    buffer.seek(0)
    consistency_chart_string = base64.b64encode(buffer.read())
    consistency_chart_uri = urllib.parse.quote(consistency_chart_string)
    
    # Duration Chart    
    practice_times = session_data[['date', 'time_minutes']].groupby('date', as_index=False).sum()
    average_practice_time_line = pd.DataFrame(data={'average': practice_times['time_minutes'].mean()}, index=range(0, practice_times.shape[0]))

    plt.figure(figsize=(18, 8))
    plt.xlabel("Practice Date", fontsize=20)
    plt.ylabel("Total Practice Time", fontsize=20)
    plt.title("Total Practice Time per Date", fontsize=30)
    plt.plot(practice_times['date'], practice_times['time_minutes'])
    plt.plot(practice_times['date'], average_practice_time_line)
    
    duration_chart = plt.gcf()
    buffer = BytesIO()
    duration_chart.savefig(buffer, format="png")
    buffer.seek(0)
    duration_chart_string = base64.b64encode(buffer.read())
    duration_chart_uri = urllib.parse.quote(duration_chart_string)
    
    context = {
        'consistency_chart': consistency_chart_uri,
        'duration_chart': duration_chart_uri,
        'days_practiced_curr_month': days_practiced_curr_month,
        'average_practice_time': average_practice_time,
        'avg_days_between_practice': avg_days_between_practice,
        'session_data': session_data,
        'days_since_last_practice': days_since_last_practice
    }
    
    return render(request, "practice_logs/dashboard.html", context)

@login_required
def view_sources(request):
    sources = Source.objects.filter(user=request.user).values()
    online_sources = sources.exclude(type="book")
    print_sources = sources.filter(type="book")
    online_source_ids = [source["id"] for source in online_sources]
    print_source_ids = [source["id"] for source in print_sources]
    online_exercises = Exercise.objects.filter(source_id__in=online_source_ids).values()
    print_exercises = Exercise.objects.filter(source_id__in=print_source_ids).values()

    context = {
        'sources': sources,
        'online_sources': online_sources,
        'print_sources': print_sources,
        'online_exercises': online_exercises,
        'print_exercises': print_exercises
    }
    
    return render(request, "practice_logs/view_sources.html", context)

@login_required
def new_source(request):
    if request.method == "POST":
        form = SourceForm(data=request.POST)
        if form.is_valid():
            new_source = form.save(commit=False)
            new_source.user = request.user
            new_source.save()
            return redirect("practice_logs:view_sources")
    else:
        form = SourceForm()
    context = {"form": form}
    return render(request, "practice_logs/new_source.html", context)

@login_required
def edit_source(request, source_id):
    source = Source.objects.get(id=source_id)
    
    if source.user != request.user:
        raise Http404
    
    if request.method == "POST":
        form = SourceForm(instance=source, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_sources")
    else:
        form = SourceForm(instance=source)
        
    context = {"form": form, "source": source}
    return render(request, "practice_logs/edit_source.html", context)

@login_required
def delete_source(request, source_id):
    source = Source.objects.get(id=source_id)
    
    if source.user != request.user:
        raise Http404
    
    source.delete()
    return redirect("practice_logs:view_sources")

@login_required
def new_print_exercise(request):
    if request.method == "POST":
        form = PrintExerciseForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_sources")
    else:
        form = PrintExerciseForm(request.user)
    context = {"form": form}
    return render(request, "practice_logs/new_print_exercise.html", context)

@login_required
def new_online_exercise(request):
    if request.method == "POST":
        form = OnlineExerciseForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_sources")
    else:
        form = OnlineExerciseForm(request.user)
    context = {"form": form}
    return render(request, "practice_logs/new_online_exercise.html", context)

@login_required
def edit_print_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)

    source = exercise.source
    if source.user != request.user:
        raise Http404
    
    if request.method == "POST":
        form = PrintExerciseForm(request.user, instance=exercise, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_sources")
    else:
        form = PrintExerciseForm(request.user, instance=exercise)
        
    context = {"form": form, "exercise": exercise}
    return render(request, "practice_logs/edit_print_exercise.html", context)

@login_required
def edit_online_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    
    source = exercise.source
    if source.user != request.user:
        raise Http404
    
    if request.method == "POST":
        form = OnlineExerciseForm(request.user, instance=exercise, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_sources")
    else:
        form = OnlineExerciseForm(request.user, instance=exercise)
        
    context = {"form": form, "exercise": exercise}
    return render(request, "practice_logs/edit_online_exercise.html", context)

@login_required
def delete_exercise(request, exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    
    source = exercise.source
    if source.user != request.user:
        raise Http404
    
    exercise.delete()
    return redirect("practice_logs:view_sources")

@login_required
def view_goals(request):
    goals = Goal.objects.filter(user=request.user)
    
    context = {
        "goals": goals
    }
    
    return render(request, "practice_logs/view_goals.html", context)

@login_required
def new_goal(request):
    if request.method == "POST":
        form = GoalsForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_goals")
    else:
        form = GoalsForm(request.user)
    context = {"form": form}
    return render(request, "practice_logs/new_goal.html", context)
    
@login_required
def edit_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    
    if goal.user != request.user:
        raise Http404
    
    if request.method == "POST":
        form = GoalsForm(request.user, instance=goal, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("practice_logs:view_goals")
    else:
        form = GoalsForm(request.user, instance=goal)
        
    context = {"form": form, "exercise": goal}
    return render(request, "practice_logs/edit_goal.html", context)

@login_required
def delete_goal(request, goal_id):
    goal = Goal.objects.get(id=goal_id)
    
    if goal.user != request.user:
        raise Http404
    
    goal.delete()
    return redirect("practice_logs:view_goals")