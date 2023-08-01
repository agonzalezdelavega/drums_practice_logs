from django.urls import path
from . import views

app = "learning_logs"

urlpatterns = [
    path("", views.index, name="index"),
    path("sessions/", views.view_sessions, name="view_sessions")
]