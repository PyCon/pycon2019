#!/bin/bash

if [ -z "$1" ]
then
    echo 'usage: rollout.sh staging|prod' >&2
    exit 2
fi

set -e

git checkout develop
git push

git checkout staging
git pull origin develop
git push

if [ "$1" = "prod" ]
then
    git checkout production
    git pull origin develop
    git push
fi

git checkout develop

if [ "$1" != "prod" ]
then
    echo
    echo '    Argument "prod" not provided, so NOT pushing to production'
    echo
fi
