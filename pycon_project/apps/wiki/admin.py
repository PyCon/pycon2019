from django import forms
from django.contrib import admin

from markitup.widgets import AdminMarkItUpWidget

from wakawaka.models import WikiPage, Revision
from wakawaka.admin import RevisionAdmin, WikiPageAdmin

class PyconRevisionAdmin(RevisionAdmin):
    raw_id_fields = ("creator", "page")
    list_filter = ("created", "modified", "page")

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "content":
            kwargs["widget"] = AdminMarkItUpWidget()
        elif db_field.name == "message":
            kwargs["widget"] = forms.Textarea(attrs={'rows': 3})
        return super(PyconRevisionAdmin, self).formfield_for_dbfield(db_field, **kwargs)


# Removes the revision inline from the wiki page admin since it doesn't work well with the editor
admin.site.unregister(WikiPage)
admin.site.register(WikiPage)

# Use the markitup widget for the revision content
admin.site.unregister(Revision)
admin.site.register(Revision, PyconRevisionAdmin)
