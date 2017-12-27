from django.contrib import admin

import reversion

from markedit.admin import MarkEditAdmin

from symposion.boxes.models import Box


class BoxAdmin(reversion.VersionAdmin, MarkEditAdmin):
    class MarkEdit:
        fields = []
        options = {
            'preview': 'below'
        }

admin.site.register(Box, BoxAdmin)
