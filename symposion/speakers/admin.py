from django.contrib import admin

from markedit.admin import MarkEditAdmin

from symposion.speakers.models import Speaker


class SpeakerAdmin(MarkEditAdmin):
    list_display = ["name", "email", "created", "twitter_username",
                    "mobile_number"]
    raw_id_fields = ["user"]
    search_fields = ["name", "email", "twitter_username"]

    class MarkEdit:
        fields = []
        options = {
            'preview': 'below'
        }

admin.site.register(Speaker, SpeakerAdmin)
