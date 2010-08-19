from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from boxes.models import Box


register = template.Library()


class BoxNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) == 2:
            label = bits[1]
            user = None
        elif len(bits) == 3:
            label = bits[1]
            user = bits[2]
        else:
            raise template.TemplateSyntaxError(
                "%s takes two or three arguments" % repr(bits[0])
            )
        return cls(label, user)
    
    def __init__(self, label, user):
        self.label = template.Variable(label)
        if user is not None:
            self.user = template.Variable(user)
        else:
            self.user = None
    
    def render(self, context):
        label = self.label.resolve(context)
        if self.user is not None:
            user = self.user.resolve(context)
        else:
            user = None
        try:
            box = Box.objects.get(label=label, user=user)
        except Box.DoesNotExist:
            try:
                box = Box.objects.get(label=label, user=None)
            except Box.DoesNotExist:
                return u""
        ctx = {"content": mark_safe(box.render())}
        return render_to_string("boxes/box.html", ctx)


@register.tag
def box(parser, token):
    return BoxNode.handle_token(parser, token)
