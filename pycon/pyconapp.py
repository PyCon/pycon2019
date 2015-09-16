from django.apps import AppConfig


class PyConConfig(AppConfig):
    name = 'pycon'

    def ready(self):
        # Import forms so they get registered with our proposal kind registry
        from . import forms  # noqa
