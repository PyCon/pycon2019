from django import forms
from django.contrib import admin

from markedit.admin import MarkEditAdmin

from pycon.models import (PyConProposalCategory, PyConSponsorTutorialProposal,
                          PyConTalkProposal, PyConTutorialProposal,
                          PyConPosterProposal, PyConLightningTalkProposal,
                          PyConOpenSpaceProposal, ScheduledEvent, EduSummitTalkProposal,
                          PyConStartupRowApplication, PyConRoomSharingRequest, PyConRoomSharingOffer,
                          SecureSubmission)


class ProposalMarkEditAdmin(MarkEditAdmin):
    class MarkEdit:
        fields = []
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
        'overall_status',
        'status',  # result.status
        'submitted',
        'speaker',
        'category',
        'audience_level',
        'domain_level',
        '_registration_count',
        'cancelled',
    ]
    list_filter = ['result__status', 'cancelled', 'category']
    list_select_related = True
    search_fields = ['title']

    def status(self, obj):
        try:
            return obj.result.status
        except:
            return "undecided"
    status.admin_order_field = 'result__status'

    def _registration_count(self, obj):
        kwargs = {'count': obj.registration_count, 'max': obj.max_attendees}
        if obj.max_attendees:
            if obj.registration_count == obj.max_attendees:
                return '<div style="color: blue;">{count} of {max}</div>'.format(**kwargs)
            elif obj.registration_count > obj.max_attendees:
                return '<div style="color: red;">{count} of {max}</div>'.format(**kwargs)
            else:
                return '{count} of {max}'.format(**kwargs)
        else:
            return '{count}'.format(**kwargs)
    _registration_count.allow_tags = True


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
        fields = []
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


class OpenSpaceAdmin(ProposalMarkEditAdmin):
    list_display = [
        'title',
        'kind',
        'status',
        'submitted',
        'speaker',
        'cancelled'
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


class ScheduledEventAdmin(MarkEditAdmin):
    list_display = [
        'name',
        'start',
        'end',
        'location',
        'published'
    ]
    list_filter = ['published']
    search_fields = ['name', 'description', 'location']
    ordering = ['-start']
    prepopulated_fields = {"slug": ("name",)}


class EduSummitTalkAdmin(ProposalMarkEditAdmin):
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

class StartupRowApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'company_name',
        'applicant',
        'created',
        'updated',
    ]

class RoomSharingOfferAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'approved'
    ]
    list_filter = ['approved']
    actions = ['approve']

    def approve(self, request, queryset):
        queryset.update(approved=True)

class RoomSharingRequestAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'approved'
    ]
    list_filter = ['approved']
    actions = ['approve']

    def approve(self, request, queryset):
        queryset.update(approved=True)

class SecureSubmissionAdmin(admin.ModelAdmin):
    def attachment_link(self, obj):
        if obj.file_attachment:
            return u"<a href='{attachment_url}'>{attachment_name}</a>".format(attachment_url=obj.attachment_url, attachment_name=obj.file_attachment_name)
        return None
    attachment_link.short_description = 'Attachment Link'
    attachment_link.allow_tags = True

    exclude = ('file_attachment', 'file_attachment_name', 'file_attachment_content_type')
    list_display = ('user', 'timestamp', 'logged', 'submission_type', 'attachment_link')
    list_filter = ('logged', 'submission_type')
    search_fields = ('user__first_name', 'user__last_name')
    readonly_fields = ('attachment_link',)


admin.site.register(PyConProposalCategory)
admin.site.register(PyConTalkProposal, TalkAdmin)
admin.site.register(PyConTutorialProposal, TutorialAdmin)
admin.site.register(PyConPosterProposal, PosterAdmin)
admin.site.register(PyConOpenSpaceProposal, OpenSpaceAdmin)
admin.site.register(PyConSponsorTutorialProposal, SponsorTutorialAdmin)
admin.site.register(PyConLightningTalkProposal, LightningTalkAdmin)
admin.site.register(EduSummitTalkProposal, EduSummitTalkAdmin)
admin.site.register(ScheduledEvent, ScheduledEventAdmin)
admin.site.register(PyConStartupRowApplication, StartupRowApplicationAdmin)
admin.site.register(PyConRoomSharingOffer, RoomSharingOfferAdmin)
admin.site.register(PyConRoomSharingRequest, RoomSharingRequestAdmin)
admin.site.register(SecureSubmission, SecureSubmissionAdmin)


from account.models import Account, EmailAddress

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class AccountInline(admin.StackedInline):
    model = Account
    extra = 0


class EmailAddressInline(admin.StackedInline):
    model = EmailAddress
    extra = 0


class HasAccountListFilter(admin.SimpleListFilter):
    title = "has associated Account"
    parameter_name = "has_account"

    def lookups(self, request, model_admin):
        return (
            (1, "Yes"),
            (0, "No"),
        )

    def queryset(self, request, queryset):
        if self.value() not in [None, ""]:
            if self.value() == "1":
                return queryset.exclude(account=None)
            if self.value() == "0":
                return queryset.filter(account=None)
        return queryset


class HasEmailAddressListFilter(admin.SimpleListFilter):
    title = "has associated EmailAddress"
    parameter_name = "has_emailaddress"

    def lookups(self, request, model_admin):
        return (
            (1, "Yes"),
            (0, "No"),
        )

    def queryset(self, request, queryset):
        if self.value() not in [None, ""]:
            if self.value() == "1":
                return queryset.exclude(emailaddress=None)
            if self.value() == "0":
                return queryset.filter(emailaddress=None)
        return queryset


class PyConUserAdmin(UserAdmin):
    inlines = list(UserAdmin.inlines) + [AccountInline, EmailAddressInline]
    search_fields = list(UserAdmin.search_fields) + ['emailaddress__email']
    list_filter = list(UserAdmin.list_filter) + [HasAccountListFilter, HasEmailAddressListFilter]
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    ordering = ('first_name', 'last_name')


admin.site.unregister(User)
admin.site.register(User, PyConUserAdmin)


# HACK HACK - monkey patch User because the username field is useless
# when using django-user-accounts
def user_unicode(self):
    # Use full name if any, else email
    return self.get_full_name() or self.email
User.__unicode__ = user_unicode

# Also monkey patch the sort order
User._meta.ordering = ['last_name', 'first_name']
