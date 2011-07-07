from django.db import models
from django.template import Template, Context

from django.contrib.auth.models import User

from markitup.fields import MarkupField


class Box(models.Model):
    
    label = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, null=True, blank=True)
    content = MarkupField()
    
    class Meta:
        verbose_name_plural = "boxes"
        unique_together = [("label", "user")]
    
    def render(self):
        """
        Render the template data through the Django templating engine.
        """
        if hasattr(self, "_rendered_content"):
            return self._rendered_content
        t = Template(self.content)
        ctx = Context({})
        self._rendered_content = t.render(ctx)
        return self._rendered_content
