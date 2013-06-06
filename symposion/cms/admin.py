from django.contrib import admin

import reversion

from .models import Page


class PageAdmin(reversion.VersionAdmin):
    list_display = [
        'title',
        'path',
        'status',
        'publish_date',
    ]


admin.site.register(Page, PageAdmin)
