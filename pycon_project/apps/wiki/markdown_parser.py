import markdown

from wiki.utils import sanitize_html


def parse(text):
    text = sanitize_html(text)
    return markdown.markdown(text, extensions=["extra"], safe_mode=False)