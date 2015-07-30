# -*- coding: utf-8 -*-
"""
sqldns.py - Prints Data Source Name on stdout

Copied, Trimmed, and Modified from django-extensions module

Copyright (c) 2007 Michael Trier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sys
from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management.color import color_style


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-R', '--router', action='store',
                    dest='router', default='default',
                    help='Use this router-database other then default'),
        make_option('-s', '--style', action='store',
                    dest='style', default=None,
                    help='DSN format style: keyvalue, uri, pgpass, all'),
        make_option('-a', '--all', action='store_true',
                    dest='all', default=False,
                    help='Show DSN for all database routes'),
        make_option('-q', '--quiet', action='store_true',
                    dest='quiet', default=False,
                    help='Quiet mode only show DSN'),
    )
    help = """Prints DSN on stdout, as specified in settings.py
    ./manage.py sqldsn [--router=<routername>] [--style=pgpass]"""

    requires_system_checks = False
    can_import_settings = True

    def handle(self, *args, **options):
        self.style = color_style()
        all_routers = options.get('all')

        if all_routers:
            routers = settings.DATABASES.keys()
        else:
            routers = [options.get('router')]

        for i, router in enumerate(routers):
            if i != 0:
                sys.stdout.write("\n")
            self.show_dsn(router, options)

    def show_dsn(self, router, options):
        dbinfo = settings.DATABASES.get(router)
        quiet = options.get('quiet')
        dsn_style = options.get('style')

        if dbinfo is None:
            raise CommandError("Unknown database router %s" % router)

        engine = dbinfo.get('ENGINE').split('.')[-1]
        dbuser = dbinfo.get('USER')
        dbpass = dbinfo.get('PASSWORD')
        dbname = dbinfo.get('NAME')
        dbhost = dbinfo.get('HOST')
        dbport = dbinfo.get('PORT')

        dsn = []

        if engine == 'postgresql_psycopg2':
            dsn.append(self.postgresql(dbhost, dbport, dbname, dbuser, dbpass, options=dbinfo.get('OPTIONS'), dsn_style=dsn_style))

        else:
            dsn.append(self.style.ERROR('Unknown database, can''t generate DSN'))

        if not quiet:
            sys.stdout.write(self.style.SQL_TABLE("DSN for router '%s' with engine '%s':\n" % (router, engine)))

        for output in dsn:
            sys.stdout.write("{}\n".format(output))

    def postgresql(self, dbhost, dbport, dbname, dbuser, dbpass, dsn_style=None, options=None):
        if dsn_style is None:
            dsnstr = "host='{0}' dbname='{2}' user='{3}'"

            if dbport is not None:
                dsnstr = dsnstr + " port='{1}'"

            dsn = dsnstr.format(dbhost,
                                dbport,
                                dbname,
                                dbuser,)

            for k, v in options.iteritems():
                dsn += " %s=%s" % (k, v)

        elif dsn_style == 'pgpass':
            if dbport is not None:
                dbport = 5432
            dsn = '{0}:{1}:{2}:{3}:{4}'.format(dbhost,
                                               dbport,
                                               dbname,
                                               dbuser,
                                               dbpass)
        else:
            raise ValueError('supplied dsn_style not supported')

        return dsn
