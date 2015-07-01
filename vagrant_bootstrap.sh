#!/usr/bin/env bash
set -e

# Add Postgresql apt repo
wget -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list

apt-get update -qqy
apt-get purge python-pip -y
apt-get install python-pip git-core postgresql-9.3 postgresql-client-9.3 postgresql-server-dev-9.3 libpq-dev python-dev make  -y
hash -r
pip install -U pip
hash -r
pip install virtualenv virtualenvwrapper
sudo -u postgres createuser --superuser vagrant || true

# We want nodejs 0.10.11 to match our Chef servers
if [ ! -e /usr/local/bin/npm ] ; then
  wget https://nodejs.org/dist/v0.10.11/node-v0.10.11-linux-x64.tar.gz
  tar xzf node-v0.10.11-linux-x64.tar.gz
  (tar cf - -C node-v0.10.11-linux-x64 .) | (tar xf - -C /usr/local)
fi

# Now we can install less
npm install -g less@1.3.3

sudo -u vagrant rsync -az /vagrant/* ~vagrant
