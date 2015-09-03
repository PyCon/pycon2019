from django.apps import AppConfig


class SymposionProposalsConfig(AppConfig):
    name = 'symposion.proposals'

    def ready(self):
        # Hook up signals now that models are done loading
        import symposion.proposals.signals
