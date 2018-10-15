#!/bin/bash
# Dump fixtures, para desarrollo.

source _variables.sh

if [ ! -d $FIXTURESDIR ]
then
  mkdir $FIXTURESDIR
else
  rm -r $FIXTURESDIR/*
fi

for app in "${APPS[@]}"
do
  $PROJECT_ROOT/manage.py dumpdata --indent=2 $app > "$FIXTURESDIR/$app.json"
  echo "dumpdata $FIXTURESDIR/$app.json"
done

# Dump sites.json
$PROJECT_ROOT/manage.py dumpdata --indent=2 sites > "$FIXTURESDIR/sites.json"
echo "dumpdata $FIXTURESDIR/sites.json"
