#!/bin/bash
# This hook is sourced after this virtualenv is deactivated.

unalias cd_project
unalias cd_apps

export PATH=$OLD_PATH
unset OLD_PATH
unset PROJECT_ROOT

# Si en vez de usar archivos conf de Django, se quiere usar
# varibales de entorno.
# export PYTHONPATH=$OLD_PYTHONPATH
# export OLD_PYTHONPATH=""
