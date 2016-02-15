"""Print out an SVG overview of the conference."""

import os
import random
import sys
from bottle import template

class Time(object):
    def __init__(self, start, end, tscale):
        self.start = start
        self.end = end
        self.tscale = tscale

    def minutes(self, time):
        hours, minutes = divmod(time, 100)
        return (hours * 60 + minutes) // self.tscale

    def __call__(self, start, end=None):
        if end is None:
            start, end = self.start, start
        return self.minutes(end) - self.minutes(start)

class Boxes(object):
    def __init__(self):
        self.coordinates = []

    def add(self, x, width, start, end):
        self.coordinates.append((x, width, start, end))

gradient_names = (
    ['12m']
    + ['{}a'.format(h) for h in range(1, 12)]
    + ['12n']
    + ['{}p'.format(h) for h in range(1, 12)]
    )

def content_of(day):
    tutorials = []
    for day in 1, 2:
        for x in range(9):
            tutorials.append()

    return locals()

def main():
    if len(sys.argv) != 2:
        print >>sys.stderr, 'usage: overview.py destination_directory'
        sys.exit(2)
    with open('overview.tpl') as f:
        template_text = f.read()
    for day, end_time in zip(range(1, 6), [1730, 2030, 2045, 2045, 2045]):
        random.seed(day)
        scope = dict(
            day=day,
            t=Time((800 if day < 3 else 700), end_time, 2),
            )
        output = template(template_text, **scope)
        path = os.path.join(sys.argv[1], 'overview{}.svg'.format(day))
        with open(path, 'w') as f:
            f.write(output.encode('utf-8'))

if __name__ == '__main__':
    main()
