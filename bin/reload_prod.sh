#!/bin/bash

# Cuando se hace un commit desde producción, con este archivo automatizara
# procesos típicos para implementar los cambios.
#
# Nodejs requiren para recursos como las fuentes

source _variables.sh

# Probar que se esta en el entorno de producción.
if [ $VIRTUALENV != $VIRTUAL_ENV_PROD ]
then
  echo "reinstall_dev.sh es solo para el entorno virtual '$VIRTUAL_ENV_PROD'"
  exit
fi

cd $PROJECT_ROOT

# Ejecutar git pull origin master.
read -p "git pull origin $BRANCH_PROD? (y/[N]) " yn
if [ "$yn" == "y" -o "$yn" == "Y" ]
then
  git pull origin $BRANCH_PROD
fi

# NPM/Yarn.
read -p "Ejecutar yarn? (y/[N]) " yn
if [ "$yn" == "y" -o "$yn" == "Y" ]
then
  # Si yarn esta instalado, ejecutarlo, de lo contrario usar npm.
  if hash yarn 2>/dev/null
  then
    yarn install
  else
    npm install
  fi
fi

# Gulp siempre lo ejecuta.
eval gulp

# Actualizar pip.
read -p "¿Actualizar pip? (y/[N]) " yn
if [ "$yn" == "y" -o "$yn" == "Y" ]
then
  pip install -r $PROJECT_ROOT/requirements/prod.txt
fi

# Backup database
read -p "¿Backup database? (y/[N]) " yn
if [ "$yn" == "y" -o "$yn" == "Y" ]
then
  $CRON_ROOT/postgres_db_backup.sh
fi

# Ejecutar migrate.
read -p "¿Ejecutar migrate? (y/[N]) " yn
if [ "$yn" == "y" -o "$yn" == "Y" ]
then
  $PROJECT_ROOT/prod_manage.py migrate
fi

# Ejecutar collectstatic.
read -p "¿Ejecutar collectstatic? (y/[N]) " yn
if [ "$yn" == "y" -o "$yn" == "Y" ]
then
  $PYTHON_EXEC $PROJECT_ROOT/prod_manage.py collectstatic --clear --noinput
fi

# Reiniciar server.
read -p "¿Reiniciar server? (y/[N]) " yn
if [ "$yn" == "y" -o "$yn" == "Y" ]
then
  sudo systemctl restart gunicorn
fi
