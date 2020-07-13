#!/bin/bash

# import .env
if [ -f .env ]; then
    export $(egrep -v '^#' .env | xargs)
fi

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
timestamp=$(date +%Y%m%d%H%M%S)

mkdir -p $script_dir/database/dumps

mysqldump -u $MYSQL_BACKUP_USERNAME -p$MYSQL_BACKUP_PASSWORD $MYSQL_DATABASE > $script_dir/database/dumps/$timestamp.sql
