from django.shortcuts import render, redirect
# from django.db.models import Sum
from .models import Source, Exercise, Session
from .forms import SessionForm, DateSearchForm
from datetime import datetime as dt, timedelta
# import pandas as pd
# import matplotlib.pyplot as plt
# from io import BytesIO
# import urllib, base64

default_start_date = dt.today() - timedelta(days=30)
default_end_date = dt.today()


def index(request):
    return render(request, "index.html")

# def new_book(request):
#     if request.method == "POST":
#         form = BookForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("view_sessions")
#     else:
#         form = BookForm()
#     context = {"form": form}
#     return render(request, "new_book.html", context)

# def new_session(request):
#     if request.method == "POST":
#         form = SessionForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("view_sessions")
#     else:
#         form = SessionForm()
#     context = {"form": form}
#     return render(request, "new_session.html", context)

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
    session_data = Session.objects.filter(date__range=[start_date, end_date]).values('date', 'time_minutes', 'exercise_id', 'bpm',
                                                                                     'days_since_last_practice').order_by('-date')
    print(session_data)
    
    # Get exercise name
    for session in session_data:
        session['exercise'] = Exercise.objects.get(id=session['exercise_id']).name
    
    context = {
        "session_data": session_data,
        "fields": fields,
        "form": form
    }
    
    return render(request, "view_sessions.html", context)
    
# def edit_session(request, session_id):
#     session = Session.objects.get(id=session_id)
    
#     if request.method == "POST":
#         form = SessionForm(instance=session, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("view_sessions")
#     else:
#         form = SessionForm(instance=session)
        
#     context = {"form": form, "session": session}
#     return render(request, "edit_session.html", context=context)

# def delete_session(request, session_id):
#     session = Session.objects.get(id=session_id)
#     session.delete()
#     return redirect("view_sessions")

# def view_books(request):
#     return render(request, "index.html")

# def view_charts(request, start_date=default_start_date, end_date=default_end_date):
#     # Session Data
#     # session_data = pd.DataFrame(list(Session.objects.values()))
#     # session_data = session_data.rename(columns={'book_id': 'book', 'time_minutes': 'time'})
#     # book_ids = list(np.unique([book_id['book_id'] for book_id in Session.objects.values('book_id')]))
#     # session_data['book'] = session_data['book'].replace(to_replace=book_ids, value=[Book.objects.get(id=book_id).name for book_id in book_ids])
#     # session_data = session_data.sort_values(by='date')
    
#     # Consistency Chart
#     # consistency_line = px.line(data_frame=session_data, x='date', y='days_since_last_practice', markers=True,
#     #                            range_y=[min(session_data['days_since_last_practice'])-0.5, max(session_data['days_since_last_practice'])+1])
#     # consistency_line.update_yaxes(dtick=1)
#     # consistency_line.update_layout(title="Days Since Last Practice Session", title_font={"size": 20},
#     #                     yaxis_title="Number of Days", xaxis_title="Practice Date", coloraxis_showscale=False,
#     #                     width=1200, height=525, font={"family": "Sans Serif", "color": "black"})
#     # consistency_chart = pi.to_html(consistency_line, auto_play=False)
    
#     consistency = pd.DataFrame(list(Session.objects.values('date', 'days_since_last_practice'))).groupby('date', as_index=False).mean()
    
#     plt.figure(figsize=(18, 8))
#     plt.xlabel('Practice Date', fontsize=12)
#     plt.ylabel('Number of Days', fontsize=12)
#     plt.title("Days Since Last Practice Session", fontsize=20)
#     plt.plot(consistency['date'], consistency['days_since_last_practice'])
    
#     consistency_chart = plt.gcf()
#     buffer = BytesIO()
#     consistency_chart.savefig(buffer, format="png")
#     buffer.seek(0)
#     consistency_chart_string = base64.b64encode(buffer.read())
#     consistency_chart_uri = urllib.parse.quote(consistency_chart_string)
    
#     # Duration Chart
#     # tpt_date = session_data[['date', 'time']].groupby('date', as_index=False).sum()
#     # duration_line = px.line(data_frame=tpt_date, x='date', y='time', markers=True, range_y=[10, max(tpt_date['time'])+10])
#     # duration_line.update_yaxes(dtick=10)
#     # duration_line.update_layout(title="Total Practice Time per Date", title_font={"size": 20},
#     #                     yaxis_title="Total Practice Time", xaxis_title="Practice Date", coloraxis_showscale=False,
#     #                     width=1200, height=525, font={"family": "Sans Serif", "color": "black"})
#     # duration_chart = pi.to_html(duration_line, auto_play=False)
    
#     practice_times = pd.DataFrame(list(Session.objects.values('date', 'time_minutes'))).groupby('date', as_index=False).sum()
#     average_practice_time = pd.DataFrame(data={'average': practice_times['time_minutes'].mean()}, index=range(0, practice_times.shape[0]))

#     plt.figure(figsize=(18, 8))
#     plt.xlabel("Practice Date", fontsize=12)
#     plt.ylabel("Total Practice Time", fontsize=12)
#     plt.title("Total Practice Time per Date", fontsize=20)
#     plt.plot(practice_times['date'], practice_times['time_minutes'])
#     plt.plot(practice_times['date'], average_practice_time)
    
#     duration_chart = plt.gcf()
#     buffer = BytesIO()
#     duration_chart.savefig(buffer, format="png")
#     buffer.seek(0)
#     duration_chart_string = base64.b64encode(buffer.read())
#     duration_chart_uri = urllib.parse.quote(duration_chart_string)
    
#     # Speed chart
#     speed = pd.DataFrame(list(Session.objects.values("date", "bpm")))
#     min_bpm, max_bpm, mode_bpm = speed["bpm"].min(), speed["bpm"].max(), speed["bpm"].mode()
#     box_plots = plt.boxplot(speed["bpm"], positions=[speed["date"].max()-timedelta(days=30), speed["date"].max()])
            
#     # Total Time Per Book
#     tpt_book = Session.objects.filter(date__range=[start_date, end_date]).values('book').annotate(time=Sum('time_minutes'))
    
#     for book in tpt_book:
#         book['book'] = Book.objects.get(id=book['book']).name
    
#     context = {
#         'consistency_chart': consistency_chart_uri,
#         'duration_chart': duration_chart_uri,
#         'tpt_book': tpt_book
#     }
    
#     return render(request, "view_charts.html", context)
