from django.urls import path
from . import views

app = "learning_logs"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("sessions/view_sessions", views.view_sessions, name="view_sessions"),
    path("sessions/new_session", views.new_session, name="new_session"),
    path("sessions/edit_session/<int:session_id>/", views.edit_session, name="edit_session"),
    path("sessions/delete_session/<int:session_id>/", views.delete_session, name="delete_session"),
]