#!/usr/bin/env bash
set -e
apt-get update -qqy
apt-get purge python-pip -y
apt-get install python-pip git-core postgresql-9.1 postgresql-client-9.1 postgresql-server-dev-9.1 libpq5 libpq-dev python-dev make -y
hash -r
pip install -U pip
hash -r
pip install virtualenv virtualenvwrapper
sudo -u postgres createuser --superuser vagrant || true

# We want nodejs 0.10.11 to match our Chef servers
if [ ! -e /usr/local/bin/npm ] ; then
  wget https://nodejs.org/dist/v0.10.11/node-v0.10.11-linux-x64.tar.gz
  tar xzf node-v0.10.11-linux-x64.tar.gz
  (tar cf - -C node-v0.10.11-linux-x64) | (tar xf - -C /usr/local)
fi

# And postgres 9.3
# TODO!

# Now we can install less
npm install -g less@1.3.3
