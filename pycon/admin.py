from django.contrib import admin

from pycon.models import PyConProposalCategory, PyConSponsorTutorialProposal,\
    PyConTalkProposal, PyConTutorialProposal, PyConPosterProposal

admin.site.register(PyConProposalCategory)

admin.site.register(
    PyConTalkProposal,
    list_display=[
        'title',
        'kind',
        'status',
        'extreme',
        'duration',
        'submitted',
        'speaker',
        'category',
        'audience_level',
        'cancelled',
    ]
)

admin.site.register(
    PyConTutorialProposal,
    list_display=[
        'title',
        'kind',
        'status',
        'submitted',
        'speaker',
        'category',
        'audience_level',
        'cancelled',
    ]
)

admin.site.register(
    PyConPosterProposal,
    list_display=[
        'title',
        'kind',
        'status',
        'submitted',
        'speaker',
        'category',
        'audience_level',
        'cancelled',
    ]
)

admin.site.register(
    PyConSponsorTutorialProposal,
    list_display=[
        'title',
        'kind',
        'status',
        'submitted',
        'speaker',
        'cancelled',
    ]
)
