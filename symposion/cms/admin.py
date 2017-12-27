from django.conf import settings
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

    if not settings.USE_I18N:
        list_display.remove('has_fr')

    def has_fr(self, page):
        return bool(page.body_fr)

    class MarkEdit:
        fields = []
        options = {
            'preview': 'below'
        }
        if not settings.USE_I18N:
            if 'body_fr' in fields:
                fields.remove('body_fr')

admin.site.register(Page, PageAdmin)
