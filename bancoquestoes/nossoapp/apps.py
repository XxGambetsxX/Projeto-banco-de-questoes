from django.apps import AppConfig


class NossoappConfig(AppConfig):
    name = 'nossoapp'

    def ready(self):
        import nossoapp.signals
