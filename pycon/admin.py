from django.contrib import admin

from markedit.admin import MarkEditAdmin

from pycon.models import (PyConProposalCategory, PyConSponsorTutorialProposal,
    PyConTalkProposal, PyConTutorialProposal, PyConPosterProposal,
    PyConLightningTalkProposal)


class ProposalMarkEditAdmin(MarkEditAdmin):
    class MarkEdit:
        fields = ['abstract', 'additional_notes', 'outline', 'more_info']
        options = {
            'preview': 'below'
        }


class TalkAdmin(ProposalMarkEditAdmin):
    list_display = [
        'title',
        'kind',
        'status',
        'duration',
        'submitted',
        'speaker',
        'category',
        'audience_level',
        'cancelled',
    ]


class TutorialAdmin(ProposalMarkEditAdmin):
    list_display = [
        'title',
        'kind',
        'status',
        'submitted',
        'speaker',
        'category',
        'audience_level',
        'domain_level',
        'cancelled',
    ]


class LightningTalkAdmin(ProposalMarkEditAdmin):
    list_display = [
        'title',
        'kind',
        'status',
        'submitted',
        'speaker',
        'cancelled',
    ]


class PosterAdmin(ProposalMarkEditAdmin):
    list_display = [
        'title',
        'kind',
        'status',
        'submitted',
        'speaker',
        'category',
        'audience_level',
        'cancelled',
    ]


class SponsorTutorialAdmin(ProposalMarkEditAdmin):
    list_display = [
        'title',
        'kind',
        'status',
        'submitted',
        'speaker',
        'cancelled',
    ]


admin.site.register(PyConProposalCategory)
admin.site.register(PyConTalkProposal, TalkAdmin)
admin.site.register(PyConTutorialProposal, TutorialAdmin)
admin.site.register(PyConPosterProposal, PosterAdmin)
admin.site.register(PyConSponsorTutorialProposal, SponsorTutorialAdmin)
admin.site.register(PyConLightningTalkProposal, LightningTalkAdmin)
