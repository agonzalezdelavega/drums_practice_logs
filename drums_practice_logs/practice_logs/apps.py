from django.apps import AppConfig


class PracticeLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'practice_logs'
    
    def ready(self):
        import practice_logs.signals