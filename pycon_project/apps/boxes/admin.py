from django.contrib import admin

from boxes.models import Box


admin.site.register(Box,
    list_display = ["label", "user", "content"]
)
