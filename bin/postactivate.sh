#!/bin/bash
# This hook is sourced after this virtualenv is activated.

if [ -n "$ZSH_VERSION" ]; then
  export PROJECT_ROOT=$(dirname $(dirname ${(%):-%N}))
elif [ -n "$BASH_VERSION" ]; then
  export PROJECT_ROOT=$(dirname $(dirname ${BASH_SOURCE[0]}))
else
  exit
fi

NODE_MODULES="$PROJECT_ROOT/node_modules/.bin/"

export OLD_PATH=$PATH
export PATH=$PROJECT_ROOT/bin:$NODE_MODULES:$OLD_PATH

alias cd_project="cd $PROJECT_ROOT"
alias cd_apps="cd $PROJECT_ROOT/src/apps"

# Si en vez de usar archivos conf de Django, se quiere usar
# varibales de entorno.
# export OLD_PYTHONPATH=$PYTHONPATH
# export PYTHONPATH=$SRC_ROOT:$APPS_ROOT:$OLD_PYTHONPATH
