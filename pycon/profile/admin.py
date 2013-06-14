from django.contrib import admin

from .models import Profile


admin.site.register(
    Profile,
    list_display=[
        'user',
        'first_name',
        'last_name',
        'phone'
    ]
)
