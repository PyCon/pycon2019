"""Print out an SVG overview of the conference."""

import random
from bottle import template

BG = '#FEF8EC'

def main():
    random.seed(1)
    with open('overview.src') as f:
        template_text = f.read()
    print template(template_text)
    return
    paths = []
    paths.append("""
<rect width="500" height="500" style="fill:'{}';stroke-width:0" />
    """.format(BG))
    paths.append("""
<rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:1;stroke:rgb(0,0,0)" />
""")
    paths.append("""
<text x="250" y="150" 
        font-family="Georgia"
        font-size="18">{}</text>
    """.format('Morning talks'))
    print WRAPPER.format(paths='\n'.join(paths))

WRAPPER = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="140mm"
   height="140mm"
   viewBox="0 0 500 500">
{paths}
</svg>
'''

if __name__ == '__main__':
    main()
