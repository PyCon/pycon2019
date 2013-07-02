import json
import os
import re

from fabric.api import cd, env, get, hide, local, put, require, run, settings, sudo, task
from fabric.colors import red
from fabric.contrib import files, project
from fabric.utils import abort, error

# Directory structure
PROJECT_ROOT = os.path.dirname(__file__)
CONF_ROOT = os.path.join(PROJECT_ROOT, 'conf')
env.project = 'pycon'
env.project_user = os.environ['LOGNAME']
env.repo = u'git@github.com:caktus/pycon'
env.shell = '/bin/bash -c'
env.disable_known_hosts = True
env.forward_agent = True
env.settings = 'symposion.settings'

@task
def staging():
    env.environment = 'staging'
    env.hosts = ['virt-nsz0jn.psf.osuosl.org']
    env.site_hostname = 'staging-pycon.python.org'
    env.branch = 'staging'
    env.db = 'psf_pycon_2014'
    env.db_host = 'pg1.osuosl.org'
    env.db_user = 'psf_pycon_2014'
    setup_path()

@task
def production():
    env.environment = 'production'
    env.hosts = ['virt-ak9lsk.psf.osuosl.org']
    env.site_hostname = 'staging-pycon.python.org'
    env.branch = 'production'
    env.db = 'psf_pycon_2014'
    env.db_host = 'pg1.osuosl.org'
    env.db_user = 'psf_pycon_2014'
    setup_path()



def setup_path():
    env.home = '/home/%(project_user)s/' % env
    env.root = '/srv/' + env.site_hostname
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
def get_db_dump(clean=True):
    """Get db dump of remote enviroment."""
    require('environment')
    if not files.exists("%(home)s/.pgpass" % env):
        abort("Please get a copy of .pgpass and put it in your home dir")
    dump_file = '%(project)s-%(environment)s.sql' % env
    flags = '-Ox'
    if clean:
        flags += 'c'
    pg_dump = 'pg_dump -h %s -U %s %s %s' % (env.db_host, env.db_user,
                                             flags, env.db)
    host = '%s@%s' % (env.user, env.hosts[0])
    # save pg_dump output to file in local home directory
    local('ssh -C %s %s > ~/%s' % (host, pg_dump, dump_file))
    local('dropdb pycon2014; createdb pycon2014')
    local('psql pycon2014 -f ~/%s' % dump_file)


@task
def get_media(root='site_media/media'):
    """Get sync of remote media."""
    rsync = 'rsync -rvaz %(user)s@%(host)s:%(media_root)s/' % env
    cmd = '%s ./%s' % (rsync, root)
    local(cmd)


@task
def load_db_dump(dump_file):
    """Load db dump on a remote environment."""
    require('environment')
    if not files.exists("%(home)s/.pgpass" % env):
        abort("Please get a copy of .pgpass and put it in your home dir")
    temp_file = os.path.join(env.home, '%(project)s-%(environment)s.sql' % env)
    put(dump_file, temp_file)
    run('psql -h %s -U %s -d %s -f %s' % (env.db_host, env.db_user, env.db, temp_file))
