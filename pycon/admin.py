from django import forms
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
    readonly_fields = ['cte_tutorial_id', 'registrants', 'max_attendees']


class LightningTalkAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LightningTalkAdminForm, self).__init__(*args, **kwargs)
        # TODO: This is a hack to populate the field...
        self.fields['category'].initial = PyConProposalCategory.objects.all()[0]
        self.fields['audience_level'].initial = PyConLightningTalkProposal.AUDIENCE_LEVEL_NOVICE

    class Meta:
        model = PyConLightningTalkProposal
        exclude = ['abstract']


class LightningTalkAdmin(MarkEditAdmin):
    class MarkEdit:
        fields = ['additional_notes']
        options = {
            'preview': 'below'
        }

    form = LightningTalkAdminForm
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


# HACK HACK - monkey patch User because the username field is useless
# when using django-user-accounts
from django.contrib.auth.models import User


def user_unicode(self):
    # Use full name if any, else email
    return self.get_full_name() or self.email
User.__unicode__ = user_unicode

# Also monkey patch the sort order
User._meta.ordering = ['last_name', 'first_name']
