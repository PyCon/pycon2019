from django.contrib import admin

from symposion.schedule.models import Schedule, Day, Room, SlotKind, Slot, \
    SlotRoom, Presentation


admin.site.register(Schedule, list_display=("section", "published"))
admin.site.register(Day, list_display=("date", "schedule",))
admin.site.register(Room, list_display=("name", "schedule"))
admin.site.register(SlotKind, list_display=("label", "schedule"))
admin.site.register(Slot, list_display=("day", "start", "end", "kind"))
admin.site.register(SlotRoom, list_display=("slot", "room"))


class PresentationAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'title',
        'speaker',
        'cancelled',
        'proposal_base',
        'kind',
        'section',
        'tutorial_attendees',
        'tutorial_max'
    )
    list_filter = (
        'section',
        'proposal_base__kind',
        'cancelled',
    )
    search_fields = (
        'title',
        'speaker__name',
        'additional_speakers__name',
        'proposal_base__title',
        'proposal_base__kind__name',
        'description',
        'abstract',
        'section__name',
    )

    def number(self, presentation):
        return presentation.proposal_base.number
    number.admin_order_field = 'proposal_base__pk'

    def kind(self, presentation):
        return presentation.proposal_base.kind

    def tutorial_attendees(self, presentation):
        if hasattr(presentation.proposal, 'registrants'):
            return presentation.proposal.registrants.all().count()
        else:
            return 'N/A'
    tutorial_attendees.short_description = 'Attendees'

    def tutorial_max(self, presentation):
        return getattr(presentation.proposal, 'max_attendees', 'N/A')
    tutorial_max.short_description = 'Attendees Max'


admin.site.register(Presentation, PresentationAdmin)
