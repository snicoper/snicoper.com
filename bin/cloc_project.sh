#!/bin/bash

# Curiosidad para contar lineas
# Requiere de cloc dnf install cloc

source _variables.sh

cloc $PROJECT_ROOT \
--exclude-dir=\
__pycache__,\
.git,\
.idea,\
.tox,\
.vscode,\
bower_components,\
compose,\
dist,\
docs,\
htmlcov,\
locale,\
logs,\
media,\
migrations,\
node_modules,\
 \
--exclude-ext=json,coverage
