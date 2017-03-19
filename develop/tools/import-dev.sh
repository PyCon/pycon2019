#!/bin/bash

set -e
"$(dirname "$0")"/import-prep.py "$@"
vagrant ssh -- cat \> schedule.csv < schedule.csv
vagrant ssh -- /vagrant/develop/tools/import-run.sh pycon
