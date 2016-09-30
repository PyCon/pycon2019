#!/bin/bash

if [ -z "$1" ]
then
    echo usage: rollout.sh yes >&2
    exit 2
fi

set -e

git checkout develop
git push

git checkout staging
git pull origin develop
git push

git checkout production
git pull origin develop
git push

git checkout develop
