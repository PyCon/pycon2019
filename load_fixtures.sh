#!/bin/bash

# Create fresh db, load fixtures in an order that works

dropdb pycon2014
createdb pycon2014
python manage.py upgradedb --execute

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
