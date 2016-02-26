#!/bin/bash

ssh pycon pg_dump -Fc '"$(cat dsn)"' |
    vagrant ssh -- pg_restore -C -d template1
