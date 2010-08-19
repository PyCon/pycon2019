from django.contrib import admin

from schedule.models import Session, Slot, Event


admin.site.register(Event)

admin.site.register(Slot,
    list_display = ["event", "start", "end", "title"]
)

admin.site.register(Session,
    list_display = ["track", "plenary", "title", "session_type", "audience_level", "cancelled"]
)