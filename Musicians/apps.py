from django.apps import AppConfig


class MusiciansConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Musicians'

    def ready(self):
        import Musicians.signals