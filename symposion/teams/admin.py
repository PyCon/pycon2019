from django.contrib import admin

import reversion

from symposion.teams.models import Team, Membership

admin.site.register(
    Team,
    list_display=['name', 'access'],
    prepopulated_fields={"slug": ("name",)},
    filter_horizontal=['permissions', 'manager_permissions'],
)


class MembershipAdmin(reversion.VersionAdmin):
    list_display = ["team", "user", "state"]
    list_filter = ["team"]
    search_fields = ["user__username"]

admin.site.register(Membership, MembershipAdmin)
