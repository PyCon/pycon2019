import datetime

from django.db import models
from django.template import Template, Context

from user_mailer.user_lists import user_lists


class EmailTemplate(models.Model):
    label = models.CharField(max_length=100)
    subject = models.TextField()
    body = models.TextField()
    
    def __unicode__(self):
        return self.label
    
    def render_subject(self, ctx=None):
        return self.render(self.subject, ctx)
    
    def render_body(self, ctx=None):
        return self.render(self.body, ctx)
    
    def render(self, content, ctx=None):
        """
        Render the template data through the Django templating engine.
        """
        if ctx is None:
            ctx = {}
        t = Template(content)
        return t.render(Context(ctx))


class Campaign(models.Model):
    from_address = models.CharField(max_length=150)
    email_template = models.ForeignKey(EmailTemplate)
    user_list = models.CharField(max_length=50, choices=[
        (l, l)
        for l, f in user_lists.iteritems()
    ])
    created = models.DateTimeField(default=datetime.datetime.now)
    sent = models.DateTimeField(null=True)
    
    def __iter__(self):
        return iter(user_lists[self.user_list]())
