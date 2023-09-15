from django import forms
from .models import Source, Exercise, Session, Goal
from datetime import datetime as dt


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = [
            "name", "type", "author"
        ]
        labels = {
            "name": "Name", "author": "Author"
        }
        widgets = {
            "type": forms.widgets.Select
        }
        
# Form for entering new exercises found in print media
class PrintExerciseForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(PrintExerciseForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.filter(user=user, type="book")
    
    class Meta:
        model = Exercise
        fields = [
            "name", "source", "page"
        ]
        labels = {
            "name": "Name", "page": "Page"
        }
        widgets = {
            "source": forms.widgets.Select
        }

# Form for entering new exercises found in online media
class OnlineExerciseForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(OnlineExerciseForm, self).__init__(*args, **kwargs)
        self.fields['source'].queryset = Source.objects.filter(user=user).exclude(type="book")
                                                               
    class Meta:
        model = Exercise
        fields = [
            "name", "source", "link"
        ]
        labels = {
            "name": "Name", "link": "URL"
        }
        widgets = {
            "source": forms.widgets.Select
        }

class SessionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        sources = Source.objects.filter(user=user)
        self.fields['exercise'].queryset = Exercise.objects.filter(source__in=sources)
    
    class Meta:
        model = Session
        fields = [
            "date", "time_minutes", "exercise", "bpm"
        ]
        labels = {
            "date": "Date", "time_minutes": "Time (minutes)", "exercise": "Exercise", "bpm": "BPM"
        }
        widgets = {
            "date": forms.DateInput(attrs={
                "type": "date",
                "value": dt.today,
                "max": dt.today
            }),
        }
        
class DateSearchForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.NumberInput(attrs={"type": "date", "value": dt.today, "required": True}), required=False)
    end_date = forms.DateField(widget=forms.widgets.NumberInput(attrs={"type": "date", "value": dt.today, "required": True}), required=False)

class GoalsForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(GoalsForm, self).__init__(*args, **kwargs)
        sources = Source.objects.filter(user=user)
        self.fields['exercise'].queryset = Exercise.objects.filter(source__in=sources)
        
    class Meta:
        model = Goal
        fields = [
            "exercise", "start_date", "end_date", "frequency", "period", "reminder"
        ]
        labels = {
            "exercise": "Exercise", "start_date": "Start Date", "end_date": "End Date", "frequency": "Frequency", "period": "Period", "reminder": "Set Reminders?"
        }
        widgets = {
            "start_date": forms.DateInput(attrs={
                "type": "date",
                "value": dt.today,
                "min": dt.today
            }),
            "end_date": forms.DateInput(attrs={
                "type": "date",
                "value": dt.today,
                "min": dt.today
            }),
            "exercise": forms.widgets.Select
        }