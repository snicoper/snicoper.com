#!/bin/bash
# Lee fixtures, para desarrollo y tests.

source _variables.sh

for app in "${APPS[@]}"
do
  # Con 4 bytes esta vacio, solo tiene []
  minsize=4
  fileseze=$(wc -c < "$PROJECT_ROOT/fixtures/$app.json")
  if [ $fileseze -gt $minsize ]
  then
    $PROJECT_ROOT/manage.py loaddata $app
  fi
done

# Dump sites.json
$PROJECT_ROOT/manage.py loaddata sites.json
