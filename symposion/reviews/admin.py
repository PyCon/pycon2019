from django.contrib import admin

from symposion.reviews.models import (
    NotificationTemplate, ProposalGroup, ProposalResult
)


admin.site.register(
    NotificationTemplate,
    list_display=[
        'label',
        'from_address',
        'subject'
    ]
)

admin.site.register(
    ProposalGroup,
    list_display=['name', 'review_start', 'vote_start', 'vote_end']
)

admin.site.register(
    ProposalResult,
    list_display=['proposal', 'status', 'score', 'vote_count', 'accepted', 'group'],
    list_filter=['proposal__kind__name'],
)
