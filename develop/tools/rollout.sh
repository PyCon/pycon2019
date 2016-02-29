#!/bin/bash

if [ -z "$1" ]
then
    echo usage: rollout.sh yes >&2
    exit 2
fi

set -e

git co staging
git pull origin develop
git push

git co production
git pull origin develop
git push

git co develop
