#!/bin/bash

source "${HOME}/.bashrc"

workon "snicopercom"

source _variables.sh

$PROJECT_ROOT/prod_manage.py clearsessions

echo "Eliminadas sesiones caducadas"
