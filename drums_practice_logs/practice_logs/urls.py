from django.urls import path
from . import views

app_name = "practice_logs"

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("sources/view_sources", views.view_sources, name="view_sources"),
    path("sources/new_source", views.new_source, name="new_source"),
    path("sources/edit_source/<int:source_id>/", views.edit_source, name="edit_source"),
    path("sources/delete_source/<int:source_id>/", views.delete_source, name="delete_source"),
    path("sources/new_print_exercise", views.new_print_exercise, name="new_print_exercise"),
    path("sources/new_online_exercise", views.new_online_exercise, name="new_online_exercise"),
    path("sources/edit_print_exercise/<int:exercise_id>/", views.edit_print_exercise, name="edit_print_exercise"),
    path("sources/edit_online_exercise/<int:exercise_id>/", views.edit_online_exercise, name="edit_online_exercise"),
    path("sources/delete_exercise/<int:exercise_id>/", views.delete_exercise, name="delete_exercise"),
    path("sessions/view_sessions", views.view_sessions, name="view_sessions"),
    path("sessions/new_session", views.new_session, name="new_session"),
    path("sessions/edit_session/<int:session_id>/", views.edit_session, name="edit_session"),
    path("sessions/delete_session/<int:session_id>/", views.delete_session, name="delete_session"),
    path("goals/view_goals", views.view_goals, name="view_goals"),
    path("goals/new_goals", views.new_goal, name="new_goal"),
    path("goals/edit_goals/<int:goal_id>/", views.edit_goal, name="edit_goal"),
    path("goals/delete_goals/<int:goal_id>/", views.delete_goal, name="delete_goal"),
    path("goals/update_goal_notifications/<int:goal_id>/", views.update_goal_notifications, name="update_goal_notifications"),
]