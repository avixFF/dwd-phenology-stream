#!/bin/bash

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
cd "$script_dir"

# import .env
if [ -f .env ]; then
    export $(egrep -v '^#' .env | xargs)
fi

timestamp=$(date +%Y%m%d%H%M%S)
dir="$script_dir/database/dumps"
num_backups=5

mkdir -p $dir

mysqldump -u $MYSQL_BACKUP_USERNAME -p$MYSQL_BACKUP_PASSWORD $MYSQL_DATABASE > $dir/$timestamp.sql

# Remove old backups, leave $num_backups most recent
ls -1tr $dir/* | head -n -$num_backups | xargs --no-run-if-empty rm
