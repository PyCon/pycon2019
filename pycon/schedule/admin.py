from django.contrib import admin

from pycon.schedule.models import Session, SessionRole


admin.site.register(Session)
admin.site.register(SessionRole)
