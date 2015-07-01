#!/usr/bin/env bash
set -e
apt-get update -qqy
apt-get purge python-pip -y
apt-get install python-pip git-core postgresql-9.1 postgresql-client-9.1 postgresql-server-dev-9.1 libpq5 libpq-dev python-dev make -y
hash -r
pip install -U pip
hash -r
pip install virtualenv virtualenvwrapper
sudo -u postgres createuser --superuser vagrant
