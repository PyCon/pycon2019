import csv
import os

from django.core.management.base import BaseCommand, CommandError

from pycon.models import PyConTalkProposal


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        csv_file = csv.writer(open(os.path.join(os.getcwd(), "proposals.csv"), "wb"))
        csv_file.writerow(['abstract', 'additional_notes', 'additional_requirements', 'audience', 'audience_level', 'category', 'category_id', 'description', 'duration', 'number', 'outline', 'overall_status', 'perceived_value', 'title', 'tags'])
        
        for proposal in PyConTalkProposal.objects.all():
            csv_file.writerow([
                proposal.abstract.encode("utf-8"),
                proposal.additional_notes.encode("utf-8"),
                proposal.additional_requirements.encode("utf-8"),
                proposal.audience.encode("utf-8"),
                proposal.audience_level,
                proposal.category.name.encode("utf-8"),
                proposal.category_id,
                proposal.description.encode("utf-8"),
                proposal.duration,
                proposal.number.encode("utf-8"),
                proposal.outline.encode("utf-8"),
                proposal.overall_status,
                proposal.perceived_value.encode("utf-8"),
                proposal.title.encode("utf-8"),
		u', '.join([tag.name for tag in proposal.tags.all()]).encode("utf-8"),
            ])
