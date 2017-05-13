#!/bin/bash

set -eux

ROOT=/eurovoter
VOTERS=$ROOT/docker/voters.txt
COUNTRIES=$ROOT/docker/countries.txt

[ -f $VOTERS -a -f $COUNTRIES ] || exit 1

DB_FILE=$HOME/state.db

cd $ROOT
./newdb.py $DB_FILE

xargs -0 -n 1 ./newvoter.py $DB_FILE < <(tr \\n \\0 <$VOTERS)
xargs -0 -n 1 ./newcountry.py $DB_FILE < <(tr \\n \\0 <$COUNTRIES)

./server.py -d -a 0.0.0.0 -p 8080 $DB_FILE
