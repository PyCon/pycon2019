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
        'section'
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
        'description',
        'abstract',
        'section__name',
    )

    def number(self, presentation):
        return presentation.proposal_base.number
    number.admin_order_field = 'proposal_base__pk'

admin.site.register(Presentation, PresentationAdmin)
