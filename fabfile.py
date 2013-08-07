import json
import os
import re

from fabric.api import cd, env, get, hide, local, put, require, run, settings, sudo, task
from fabric.colors import red
from fabric.contrib import files, project
from fabric.utils import abort, error

# Directory structure
PROJECT_ROOT = os.path.dirname(__file__)
env.project = 'pycon'
env.project_user = os.environ['LOGNAME']
env.shell = '/bin/bash -c'
env.settings = 'symposion.settings'

@task
def staging():
    env.environment = 'staging'
    env.hosts = ['virt-nsz0jn.psf.osuosl.org']
    env.site_hostname = 'staging-pycon.python.org'
    env.root = '/srv/staging-pycon.python.org'
    env.branch = 'staging'
    env.db = 'psf-pycon-2014-staging'
    env.db_host = 'pg1.osuosl.org'
    env.db_user = 'psf-pycon-2014-staging'
    setup_path()

@task
def production():
    env.environment = 'production'
    env.hosts = ['virt-ak9lsk.psf.osuosl.org']
    env.site_hostname = 'us.pycon.org'
    env.root = '/srv/staging-pycon.python.org'
    env.branch = 'production'
    env.db = 'psf_pycon_2014'
    env.db_host = 'pg1.osuosl.org'
    env.db_user = 'psf_pycon_2014'
    setup_path()


def setup_path():
    env.home = '/home/%(project_user)s/' % env
    env.code_root = os.path.join(env.root, 'current')
    env.virtualenv_root = os.path.join(env.root, 'shared/env')
    env.media_root = os.path.join(env.root, 'shared', 'media')

@task
def manage_run(command, sudo=False):
    """Run a Django management command on the remote server."""
    require('environment')
    manage_base = u"%(virtualenv_root)s/bin/python %(code_root)s/manage.py " % env
    with cd(env.code_root):
        if sudo:
            sudo(u'%s %s' % (manage_base, command))
        else:
            run(u'%s %s' % (manage_base, command))

@task
def manage_shell():
    """Drop into the remote Django shell."""
    manage_run("shell")

@task
def deploy():
    """Deploy to a given environment."""
    # NOTE: chef will check every 30 minutes or so whether the
    # repo has changed, and if so, redeploy.  Or you can use this
    # to make it run immediately.
    require('environment')
    sudo('chef-client')

@task
def ssh():
    """Ssh to a given server"""
    require('environment')
    local("ssh %s" % env.hosts[0])

@task
def get_db_dump(dbname, clean=True):
    """Overwrite your local `dbname` database with the data from the server.
    The name of your local db is required as an argument, e.g.:

        fab staging get_db_dump:dbname=mydbname

    """
    require('environment')
    if not files.exists("%(home)s/.pgpass" % env):
        abort("Please get a copy of .pgpass and put it in your home dir on the server of interest (not your local system)")
    dump_file = '%(project)s-%(environment)s.sql' % env
    flags = '-Ox'
    if clean:
        flags += 'c'
    pg_dump = 'pg_dump -h %s -U %s %s %s' % (env.db_host, env.db_user,
                                             flags, env.db)
    host = '%s@%s' % (env.user, env.hosts[0])
    # save pg_dump output to file in local home directory
    local('ssh -C %s %s > ~/%s' % (host, pg_dump, dump_file))
    local('dropdb %s; createdb %s' % (dbname, dbname))
    local('psql %s -f ~/%s' % (dbname, dump_file))


@task
def get_media(root='site_media/media'):
    """Syncs media files from server to a local dir.
    Defaults to ./site_media/media; you can override by passing
    a different relative path as root:

        fab server get_media:root=my_dir/media/foo

    Local dir ought to exist already.
    """
    rsync = 'rsync -rvaz %(user)s@%(host)s:%(media_root)s/' % env
    cmd = '%s ./%s' % (rsync, root)
    local(cmd)


@task
def load_db_dump(dump_file):
    """Given a dump on your home dir on the server, load it to the server's
    database, overwriting any existing data.  BE CAREFUL!"""
    require('environment')
    if not files.exists("%(home)s/.pgpass" % env):
        abort("Please get a copy of .pgpass and put it in your home dir")
    temp_file = os.path.join(env.home, '%(project)s-%(environment)s.sql' % env)
    put(dump_file, temp_file)
    run('psql -h %s -U %s -d %s -f %s' % (env.db_host, env.db_user, env.db, temp_file))

@task
def make_messages():
    """Extract English text from code and templates, and update the
    .po files for translators to translate"""
    # Make sure gettext is installed
    local("gettext --help >/dev/null 2>&1")
    if os.path.exists("locale/fr/LC_MESSAGES/django.po"):
        local("python manage.py makemessages -a")
    else:
        local("python manage.py makemessages -l fr")

@task
def compile_messages():
    """Compile the translated .po files into more efficient .mo
        files for runtime use"""
    # Make sure gettext is installed
    local("gettext --help >/dev/null 2>&1")
    local("python manage.py compilemessages")
