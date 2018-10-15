#!/bin/bash

# Crea un backup de la db, es necesario tener el archivo ~/.pgpass.
# hostname:port:database:username:password
# Tener el archivo ~/.pgpass con permisos chmod 600.
# Crea los backups en $backup_dir.
# Elimina los backups con mas de $number_of_days días

source $HOME/.bashrc

workon "snicopercom"

source _variables.sh

if [ ! -d "$PROD_DATABASE_BACKUP_DIR" ]; then
  mkdir -p $PROD_DATABASE_BACKUP_DIR
fi

# Numbers of days you want to keep copie of your databases.

pg_dump -U $PROD_DATABASE_USER --no-password $PROD_DATABASE_NAME > $PROD_DATABASE_BACKUP_DIR$PROD_DATABASE_NAME.$PROD_DATABASE_BACKUP_DATE.psql

# Eliminar copias con mas 'number_of_days' días.
find $PROD_DATABASE_BACKUP_DIR -type f -prune -mtime +$PROD_DATABASE_NUMBER_OF_DAYS -exec rm -f {} \;

echo "Backup de la db realizado con éxito"
