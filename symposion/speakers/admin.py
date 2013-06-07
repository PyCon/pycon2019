from django.contrib import admin

from markedit.admin import MarkEditAdmin

from symposion.speakers.models import Speaker


class SpeakerAdmin(MarkEditAdmin):
    list_display = ["name", "email", "created", "twitter_username"]
    search_fields = ["name", "twitter_username"]

    class MarkEdit:
        fields = ['biography', ]
        options = {
            'preview': 'below'
        }

admin.site.register(Speaker, SpeakerAdmin)
