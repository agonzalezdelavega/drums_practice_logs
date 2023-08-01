from django.shortcuts import render, redirect
from .models import Source, Exercise, Session
from .forms import SessionForm, DateSearchForm
from datetime import datetime as dt, timedelta
import calendar
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64

default_start_date = dt.today() - timedelta(days=30)
default_end_date = dt.today()


def index(request):
    return render(request, "index.html")

def new_session(request):
    if request.method == "POST":
        form = SessionForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_sessions")
    else:
        form = SessionForm()
    context = {"form": form}
    return render(request, "new_session.html", context)

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
    
    # Session Data
    session_data = Session.objects.filter(date__range=[start_date, end_date]).values('id', 'date', 'time_minutes', 'exercise_id', 'bpm',
                                                                                     'days_since_last_practice').order_by('-date')
    # Get exercise name
    for session in session_data:
        session['exercise'] = Exercise.objects.get(id=session['exercise_id']).name
    
    context = {
        "session_data": session_data,
        "fields": fields,
        "form": form
    }
    
    return render(request, "view_sessions.html", context)
    
def edit_session(request, session_id):
    session = Session.objects.get(id=session_id)
    
    if request.method == "POST":
        form = SessionForm(instance=session, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("view_sessions")
    else:
        form = SessionForm(instance=session)
        
    context = {"form": form, "session": session}
    return render(request, "edit_sessions.html", context)

def delete_session(request, session_id):
    session = Session.objects.get(id=session_id)
    session.delete()
    return redirect("view_sessions")

def dashboard(request):
    session_data = pd.DataFrame(list(Session.objects.values('date', 'time_minutes', 'days_since_last_practice')))
    curr_month = dt.strftime(dt.today(), "%Y-%m")
    days_of_month = calendar.monthrange(int(curr_month[0:4]),int(curr_month[5:]))[1]
    first_day_of_month = f"{curr_month}-01"
    last_day_of_month = f"{curr_month}-{days_of_month}"
    
    days_practiced_curr_month = Session.objects.filter(date__range=[first_day_of_month, last_day_of_month]).count()
    average_practice_time = round(session_data.groupby('date', as_index=False).sum()["time_minutes"].mean())
    avg_days_between_practice = round(session_data.groupby('date', as_index=False).min()["days_since_last_practice"].mean())
    
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
    practice_times = pd.DataFrame(list(Session.objects.values('date', 'time_minutes'))).groupby('date', as_index=False).sum()
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
    
    # User statics

    context = {
        'consistency_chart': consistency_chart_uri,
        'duration_chart': duration_chart_uri,
        'days_practiced_curr_month': days_practiced_curr_month,
        'average_practice_time': average_practice_time,
        'avg_days_between_practice': avg_days_between_practice
    }
    
    return render(request, "dashboard.html", context)
