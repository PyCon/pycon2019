from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.template import loader, Context
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode


class MarkEdit(forms.Textarea):

    def render(self, name, value, attrs=None):

        # Prepare values
        attrs = self.build_attrs(attrs, name=name)
        if not value:
            value = ''

        options = getattr(settings, 'MARKEDIT_DEFAULT_SETTINGS', {})

        if 'options' in attrs:
            options = self._eval_value(attrs['options'], {})
            del attrs['options']

        # Render widget to HTML
        t = loader.get_template('markedit/ui.html')
        c = Context({
            'attributes': self._render_attrs(attrs),
            'value': conditional_escape(force_unicode(value)),
            'id': attrs['id'],
            'options': options,
        })

        return t.render(c)

    def _eval_value(self, value, default_value):
        v = None
        try:
            v = value()
        except:
            v = value
        if v is None:
            v = default_value
        return v

    def _render_attrs(self, attrs):
        atts = u''
        for key, value in attrs.items():
            atts += u'%s="%s" ' % (key, value)
        return atts[:-1]


class AdminMarkEdit(admin_widgets.AdminTextareaWidget, MarkEdit):
    pass
