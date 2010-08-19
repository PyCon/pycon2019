from django.contrib import admin

from proposals.models import Proposal


admin.site.register(Proposal,
    list_display = ["title", "session_type", "audience_level", "cancelled"]
)