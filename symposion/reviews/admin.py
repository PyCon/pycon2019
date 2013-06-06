from django.contrib import admin

from symposion.reviews.models import NotificationTemplate


admin.site.register(
    NotificationTemplate,
    list_display=[
        'label',
        'from_address',
        'subject'
    ]
)
