"""Print out an SVG overview of the conference."""

import os
import random
import sys
from bottle import template

BG = '#FEF8EC'

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, 'usage: overview.py destination_directory'
        sys.exit(2)
    random.seed(1)
    with open('overview.src') as f:
        template_text = f.read()
    for i in range(1, 6):
        output = template(template_text, day=i)
        path = os.path.join(sys.argv[1], 'overview{}.svg'.format(i))
        with open(path, 'w') as f:
            f.write(output)

if __name__ == '__main__':
    main()
