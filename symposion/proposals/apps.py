from django.apps import AppConfig


class SymposionProposalsConfig(AppConfig):
    name = 'symposion.proposals'

    def ready(self):
        # Hook up signals now that models are done loading
        # Note: This import does the hooking up and is NOT
        # a no-op!
        import symposion.proposals.signals  # no-qa
