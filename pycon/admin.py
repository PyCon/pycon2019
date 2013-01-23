from django.contrib import admin

from pycon.models import PyConProposalCategory, PyConSponsorTutorialProposal, PyConTalkProposal, PyConTutorialProposal, PyConPosterProposal

admin.site.register(PyConProposalCategory)
admin.site.register(PyConTalkProposal)
admin.site.register(PyConTutorialProposal)
admin.site.register(PyConPosterProposal)
admin.site.register(PyConSponsorTutorialProposal)
