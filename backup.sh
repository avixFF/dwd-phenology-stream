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

mkdir -p "$dir"

if [ -z $MYSQL_PASSWORD ]; then
    mysqldump -u $MYSQL_BACKUP_USERNAME $MYSQL_DATABASE > "$dir/$timestamp.sql"
else
    mysqldump -u $MYSQL_BACKUP_USERNAME -p$MYSQL_BACKUP_PASSWORD $MYSQL_DATABASE > "$dir/$timestamp.sql"
fi

# Remove old backups, leave $num_backups most recent
count=$(ls -1tr "$dir" | wc -l)
n=$(expr $count - $num_backups)

if [ "$n" -gt 0 ]; then
    ls -1tr "$dir"/* | head -n $n | xargs -I{lin} echo \"{lin}\" | xargs rm
fi
