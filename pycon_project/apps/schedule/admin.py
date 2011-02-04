from django.contrib import admin

from schedule.models import Session, Slot


admin.site.register(Slot,
    list_display = ["pk", "start", "end", "track"]
)

admin.site.register(Session,
    list_display = ["title", "slot", "session_type", "audience_level", "cancelled"]
)