"""
Management command to make sure the permissions exist
for all kinds of proposals.
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        from symposion.proposals.kinds import ensure_proposal_records

        ensure_proposal_records()
