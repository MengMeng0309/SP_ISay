from django.apps import AppConfig


class IsayConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'isay'

    def ready(self):
        import isay.signals
