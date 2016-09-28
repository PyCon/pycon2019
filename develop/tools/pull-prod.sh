#!/bin/bash
#
# then run:
# alter database "pycon-prod" rename to pycon2016;

ssh pycon pg_dump -Fc '"$(cat dsn)"' |
    vagrant ssh -- pg_restore -d template1 --create --clean

vagrant ssh -- psql template1 <<EOF

drop database "pycon";
alter database "pycon-prod" rename to pycon;

EOF
