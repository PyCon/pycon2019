import markdown

from wiki.utils import sanitize_html


def parse(text):
    text = markdown.markdown(text, extensions=["extra"], safe_mode=False)
    return sanitize_html(text)
