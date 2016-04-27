#!/bin/bash
#
# then run:
# alter database "pycon-prod" rename to pycon2016;

ssh pycon pg_dump -Fc '"$(cat dsn)"' |
    vagrant ssh -- pg_restore -d template1 --create --clean

echo 'alter database "pycon-prod" rename to pycon2016;' |
    vagrant ssh -- psql template1
