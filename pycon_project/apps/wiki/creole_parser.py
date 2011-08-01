import re

from django.core.urlresolvers import reverse, NoReverseMatch

from biblion.creole_parser import HtmlEmitter, Parser, Rules

class WakaWakaHtmlEmitter(HtmlEmitter):
    def link_emit(self, node):
        target = node.content
        if node.children:
            inside = self.emit_children(node)
        else:
            inside = self.html_escape(target)

        try:
            target = reverse('wakawaka_page', kwargs={'slug': target})
            return u'<a href="%s">%s</a>' % (target, inside)
        except NoReverseMatch:
            return u'<a href="%s">%s</a>' % (
                self.attr_escape(target), inside)


def parse(text, emitter=WakaWakaHtmlEmitter):
    return emitter(Parser(text).parse()).emit()
