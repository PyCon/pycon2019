from django.apps import AppConfig


class SymposionProposalsConfig(AppConfig):
    name = 'symposion.proposals'

    def ready(self):
        # Hook up signals now that models are done loading
        from symposion.proposals.signals import connect_signals

        connect_signals()
