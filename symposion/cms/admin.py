from django.contrib import admin

import reversion

from markedit.admin import MarkEditAdmin

from .models import Page


class PageAdmin(reversion.VersionAdmin, MarkEditAdmin):
    list_display = [
        'title',
        'path',
        'status',
        'has_fr',
        'publish_date',
    ]

    def has_fr(self, page):
        return bool(page.body_fr)

    class MarkEdit:
        fields = ['body', 'body_fr']
        options = {
            'preview': 'below'
        }

admin.site.register(Page, PageAdmin)
