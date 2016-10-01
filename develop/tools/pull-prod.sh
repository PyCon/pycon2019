#!/bin/bash

# This presumes that you (a) have an alias set up so that you can "ssh
# pycon" to connect to our production machine, and (b) that you have the
# development environment up and running and can succcessfully "vagrant
# ssh" to talk to it.

ssh pycon pg_dump -Fc '"$(cat dsn)"' |
    vagrant ssh -- pg_restore -d template1 --create --clean

vagrant ssh -- psql template1 <<EOF

drop database "pycon";
alter database "pycon-prod" rename to pycon;

sudo mkdir -p /vagrant/site_media/media
chown vagrant.vagrant /vagrant/site_media/media

EOF

# ssh pycon tar cf - -C /srv/pycon/media sponsor_files |
#     vagrant ssh -- tar xvf - -C /vagrant/site_media/media
