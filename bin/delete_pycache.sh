#!/bin/bash

# Elimina los directorios __pycache__

source _variables.sh

find $PROJECT_ROOT -name "__pycache__" -exec rm -rf {} \;

echo "Eliminados los directorios __pycache__"
