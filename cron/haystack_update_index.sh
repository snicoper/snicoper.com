#!/bin/bash

source "${HOME}/.bashrc"

workon "snicopercom"

source _variables.sh

$PROJECT_ROOT/prod_manage.py update_index
