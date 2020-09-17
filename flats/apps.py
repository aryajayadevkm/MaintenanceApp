from django.apps import AppConfig


class FlatConfig(AppConfig):
    name = 'flats'

    def ready(self):
        import flats.signals
        from .scheduler import start
        start()