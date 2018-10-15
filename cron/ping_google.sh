#!/bin/bash

source "${HOME}/.bashrc"

workon "snicopercom"

source _variables.sh

python $PROJECT_ROOT/ping_google.py
