from django.apps import AppConfig


class ISLIdeasConfig(AppConfig):
    name = 'ideas'

    def ready(self):
        import ideas.signals
