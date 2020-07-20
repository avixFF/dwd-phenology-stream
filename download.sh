#!/bin/bash

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
cd "$script_dir"

# import .env
if [ -f .env ]; then
    export $(egrep -v '^#' .env | xargs)
fi

server="$MYSQL_BACKUP_USER@$MYSQL_BACKUP_HOST"

source=$server:/home/deploy/app/database/dumps/'$(ls -t ~/app/database/dumps | head -1)'
destination="$script_dir/database/dumps"

ssh $server 'bash app/backup.sh'
rsync "$source" "$destination"

file=$(ls "$destination" | tail -n 1)

echo "Database dump has been made and downloaded: $file (in $destination)"
