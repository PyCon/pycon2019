from django.contrib import admin

import reversion

from markedit.admin import MarkEditAdmin

from .models import Page


class PageAdmin(reversion.VersionAdmin, MarkEditAdmin):
    list_display = [
        'title',
        'path',
        'status',
        'publish_date',
    ]

    class MarkEdit:
        fields = ['body', ]
        options = {
            'preview': 'below'
        }

admin.site.register(Page, PageAdmin)
