
from django import forms

from django.contrib import admin

from pycon.mentorship.models import (
    MentorshipAvailability,
    MentorshipMentee,
    MentorshipMentor,
    MentorshipSession,
    MentorshipSlot,
)

class MentorshipSlotAdmin(admin.ModelAdmin):
    list_display = ['time']

class MentorshipMentorAdmin(admin.ModelAdmin):
    list_display = ['user']

class MentorshipMenteeAdmin(admin.ModelAdmin):
    list_display = ['user', 'responded']
    list_filter = ['responded']

class MentorshipAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['mentor', 'slot_time', 'viable']

class MentorshipSessionAdmin(admin.ModelAdmin):
    list_filter = ['finalized']
    list_display = ['__unicode__', 'slot_time', 'finalized', 'mentors_count', 'mentees_count']
    filter_horizontal = ('mentors', 'mentees',)

admin.site.register(MentorshipSlot, MentorshipSlotAdmin)
admin.site.register(MentorshipMentor, MentorshipMentorAdmin)
admin.site.register(MentorshipMentee, MentorshipMenteeAdmin)
admin.site.register(MentorshipAvailability, MentorshipAvailabilityAdmin)
admin.site.register(MentorshipSession, MentorshipSessionAdmin)
