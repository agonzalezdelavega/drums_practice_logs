from django.apps import AppConfig


class LearningLogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'learning_logs'
    
    def ready(self):
        import learning_logs.signals