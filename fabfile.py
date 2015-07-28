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
env.use_ssh_config = True

@task
def staging():
    env.environment = 'staging'
    env.hosts = ['pycon-staging.iad1.psf.io']
    env.site_hostname = 'staging-pycon.python.org'
    env.root = '/srv/pycon'
    env.branch = 'staging'
    setup_path()

@task
def production():
    env.environment = 'production'
    env.hosts = ['pycon-prod.iad1.psf.io']
    env.site_hostname = 'us.pycon.org'
    env.root = '/srv/pycon'
    env.branch = 'production'
    setup_path()


def setup_path():
    env.home = '/home/psf-users/%(project_user)s/' % env
    env.code_root = os.path.join(env.root, 'pycon')
    env.virtualenv_root = os.path.join(env.root, 'env')
    env.media_root = os.path.join(env.root, 'media')


@task
def manage_run(command):
    """Run a Django management command on the remote server."""
    require('environment')
    manage_cmd = ("{env.virtualenv_root}/bin/python "
        "manage.py {command}").format(env=env, command=command)
    dotenv_path = os.path.join(env.root, 'shared')
    with cd(env.code_root):
        sudo(manage_cmd)


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
    sudo('salt-call state.highstate')

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
    run('sudo -u pycon /srv/pycon/env/bin/python /srv/pycon/pycon/manage.py sqldsn -q -s pgpass -R default 2>/dev/null > ~/.pgpass')
    run('chmod 600 ~/.pgpass')
    dump_file = '%(project)s-%(environment)s.sql' % env
    flags = '-Ox'
    dsn = sudo('/srv/pycon/env/bin/python /srv/pycon/pycon/manage.py sqldsn -q -R default 2>/dev/null', user='pycon').stdout
    if clean:
        flags += 'c'
    pg_dump = 'pg_dump "%s" %s' % (dsn, flags)
    host = '%s@%s' % (env.user, env.hosts[0])
    # save pg_dump output to file in local home directory
    local('ssh -C %s \'%s\' > ~/%s' % (host, pg_dump, dump_file))
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
    run('sudo -u pycon /srv/pycon/env/bin/python /srv/pycon/pycon/manage.py sqldsn -q -s pgpass -R default 2>/dev/null > ~/.pgpass')
    run('chmod 600 ~/.pgpass')
    temp_file = os.path.join(env.home, '%(project)s-%(environment)s.sql' % env)
    put(dump_file, temp_file)
    dsn = sudo('/srv/pycon/env/bin/python /srv/pycon/pycon/manage.py sqldsn -q -R default 2>/dev/null', user='pycon').stdout
    run('psql "%s" -f %s' % (dsn, temp_file))

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
