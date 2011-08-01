import html5lib
from html5lib import html5parser, sanitizer


def sanitize_html(stream):
    
    bits = []
    parser = html5parser.HTMLParser(tokenizer=sanitizer.HTMLSanitizer)
    for token in parser.parseFragment(stream).childNodes:
        bits.append(token.toxml())
    return "".join(bits)
