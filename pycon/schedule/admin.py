from django.contrib import admin

from pycon.schedule.models import Session, SessionRole, SlidesUpload


class SessionAdmin(admin.ModelAdmin):
    filter_horizontal = ['slots']
    list_display = ['day', '_slots']
    list_filter = ['day']

    def _slots(self, obj):
        return ", ".join([str(slot) for slot in obj.slots.all()])


class SessionRoleAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'session':
            kwargs['queryset'] = Session.objects.order_by('day__date')
        return super(SessionRoleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class SliesUploadAdmin(admin.ModelAdmin):

    list_display = ['presentation', 'slides']


admin.site.register(Session, SessionAdmin)
admin.site.register(SessionRole, SessionRoleAdmin)
admin.site.register(SlidesUpload, SliesUploadAdmin)
