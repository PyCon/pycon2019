dropdb pycon2014; createdb pycon2014 && gondor sqldump primary |./manage.py dbshell && ./manage.py upgradedb -e

