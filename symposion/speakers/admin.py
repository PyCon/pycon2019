from django.contrib import admin

from symposion.speakers.models import Speaker


admin.site.register(
    Speaker,
    list_display=["name", "email", "created", "twitter_username"],
    search_fields=["name", "twitter_username"],
)
