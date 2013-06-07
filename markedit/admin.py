from django.contrib import admin
from markedit.widgets import AdminMarkEdit


class MarkEditAdmin(admin.ModelAdmin):

    class MarkEdit:
        fields = ['text', ]
        options = {}

    class Media:
        css = {'all': ('css/jquery-ui-1.10.3.min.css', 'css/jquery.markedit.css', )}
        js = ('js/jquery.admin.js',
              'js/jquery-ui-1.10.3.custom.min.js',
              'js/jquery.markedit.js',
              'js/showdown.js', )

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(MarkEditAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name in self.MarkEdit.fields:
            formfield.widget = AdminMarkEdit(attrs={
                'options': self.MarkEdit.options,
            })
        return formfield
