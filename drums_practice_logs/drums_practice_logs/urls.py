from django.urls import path, include

urlpatterns = [
    path('', include('practice_logs.urls')),
    path('users/', include('users.urls'))
]
