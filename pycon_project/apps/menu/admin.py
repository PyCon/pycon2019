from django.contrib import admin

from mptt.admin import MPTTModelAdmin

from menu.models import MenuItem


class MenuItemAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "login_required", "published",)

admin.site.register(MenuItem, MenuItemAdmin)
