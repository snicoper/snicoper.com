#!/bin/bash

source _variables.sh

# Probar que se esta en el entorno de desarrollo.
if [ $VIRTUALENV != $VIRTUAL_ENV_DEV ]
then
  echo "delete_migrations.sh es solo para el entorno virtual '$VIRTUAL_ENV_DEV'"
  exit
fi

find $APPS_ROOT -path "*/migrations/*.py" -not -name "__init__.py" -delete

$PYTHON_EXEC $PROJECT_ROOT/manage.py makemigrations
