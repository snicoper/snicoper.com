#!/bin/bash

# Crea un backup del directorio media.
# Crea los backups en $backup_dir.
# Elimina los backups con mas de $number_of_days días

source $HOME/.bashrc

workon "snicopercom"

source _variables.sh

if [ ! -d "$MEDIA_BACKUP_DIR/$MEDIA_BACKUP_DATE" ]
then
  mkdir -p $MEDIA_BACKUP_DIR/$MEDIA_BACKUP_DATE
  cp -r $SRC_ROOT/media/* $MEDIA_BACKUP_DIR/$MEDIA_BACKUP_DATE
fi

# Eliminar copias con mas 'number_of_days' días.
find $MEDIA_BACKUP_DIR/* -mtime +$MEDIA_NUMBER_OF_DAYS -delete

echo "Backup del directorio media en $MEDIA_BACKUP_DIR/$MEDIA_BACKUP_DATE realizado con éxito"
