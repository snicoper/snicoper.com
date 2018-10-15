#!/bin/bash

# Cambia/se asegura, de los permisos en el sitio,
# Todos los archivos con permisos 644 y todos los
# directorios 755.
# Algunos archivos necesitan permisos de ejecución.

source _variables.sh

# drwxrwxr-x
FOLDERS_PERMS=775

# -rw-rw-r--
FILES_PERMS=664

# Por defecto excluye directorios bower_components(bower) y node_modules(node)
echo "Cambiando permisos de directorios $FOLDERS_PERMS"
find $PROJECT_ROOT -type d ! -path "*/bower_components/*" ! -path "*/node_modules/*" ! -path "*/.tox/*" -exec chmod $FOLDERS_PERMS {} \;
echo "Cambiando permisos de archivos $FILES_PERMS"
find $PROJECT_ROOT -type f ! -path "*/bower_components/*" ! -path "*/node_modules/*" ! -path "*/.tox/*" -exec chmod $FILES_PERMS {} \;

########################
# Permisos de ejecución.
########################

####################################################################################################
# BIN_ROOT
####################################################################################################
echo "Cambiando permisos de ejecución a $BIN_ROOT/createapp.sh"
chmod +x "$BIN_ROOT/createapp.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/cloc_project.sh"
chmod +x "$BIN_ROOT/cloc_project.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/delete_migrations.sh"
chmod +x "$BIN_ROOT/delete_migrations.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/delete_pycache.sh"
chmod +x "$BIN_ROOT/delete_pycache.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/django_dumpdata.sh"
chmod +x "$BIN_ROOT/django_dumpdata.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/django_loaddata.sh"
chmod +x "$BIN_ROOT/django_loaddata.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/gunicorn_start.sh"
chmod +x "$BIN_ROOT/gunicorn_start.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/permissions.sh"
chmod +x "$BIN_ROOT/permissions.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/reinstall_dev.sh"
chmod +x "$BIN_ROOT/reinstall_dev.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/reload_prod.sh"
chmod +x "$BIN_ROOT/reload_prod.sh"

echo "Cambiando permisos de ejecución a $BIN_ROOT/runserver.sh"
chmod +x "$BIN_ROOT/runserver.sh"

####################################################################################################
# SRC_ROOT
####################################################################################################
echo "Cambiando permisos de ejecución a $SRC_ROOT/manage.py"
chmod +x "$PROJECT_ROOT/manage.py"

echo "Cambiando permisos de ejecución a $SRC_ROOT/prod_manage.py"
chmod +x "$PROJECT_ROOT/prod_manage.py"

echo "Cambiando permisos de ejecución a $SRC_ROOT/test_manage.py"
chmod +x "$PROJECT_ROOT/test_manage.py"

####################################################################################################
# CRON_ROOT
####################################################################################################
echo "Cambiando permisos de ejecución a $CRON_ROOT/clear_sessions.sh"
chmod +x "$CRON_ROOT/clear_sessions.sh"

echo "Cambiando permisos de ejecución a $CRON_ROOT/haystack_update_index.sh"
chmod +x "$CRON_ROOT/haystack_update_index.sh"

echo "Cambiando permisos de ejecución a $CRON_ROOT/media_backup.sh"
chmod +x "$CRON_ROOT/media_backup.sh"

echo "Cambiando permisos de ejecución a $CRON_ROOT/ping_google.sh"
chmod +x "$CRON_ROOT/ping_google.sh"

echo "Cambiando permisos de ejecución a $CRON_ROOT/postgres_db_backup.sh"
chmod +x "$CRON_ROOT/postgres_db_backup.sh"

echo "Terminado el cambio de permisos."
