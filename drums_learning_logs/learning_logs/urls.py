from django.urls import path
from . import views

app = "learning_logs"

urlpatterns = [
    path("", views.index, name="index"),
]