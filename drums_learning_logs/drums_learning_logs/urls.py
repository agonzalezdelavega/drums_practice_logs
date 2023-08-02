from django.urls import path, include

urlpatterns = [
    path('', include('learning_logs.urls')),
    path('users/', include('users.urls'))
]
