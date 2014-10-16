#!/bin/bash

# Create fresh db, load fixtures in an order that works

read -p "About to blow away DB - answer Y to go ahead, ^C to cancel> "
case $REPLY in
  Y*) ;;
  *)
   echo "Cancelling (try capital Y if you meant to go ahead)"
   exit 1
  ;;
esac

dropdb pycon2015
createdb pycon2015
python manage.py syncdb --noinput
python manage.py migrate

python manage.py loaddata \
  fixtures/auth_user.json \
  fixtures/initial_data.json \
  fixtures/pycon.json \
  fixtures/cms_initial_pages.json \
  fixtures/conference.json \
  fixtures/initial_boxes.json \
  fixtures/initial_data.json \
  fixtures/proposal_base.json \
  fixtures/sitetree_menu.json \
  fixtures/sponsorship_benefits.json \
  fixtures/sponsorship_levels.json \
  fixtures/tutorials_schedule.json \
  fixtures/talks_schedule.json \
  fixtures/permissions.json \
  fixtures/teams.json \

echo
echo
echo "Database initialized."
echo "Hint: setup an account with: ./manage.py createsuperuser"
