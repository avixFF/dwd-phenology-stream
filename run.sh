#!/bin/bash

# import .env
if [ -f .env ]; then
    export $(egrep -v '^#' .env | xargs)
fi

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
pipenv=/usr/local/bin/pipenv
log_file=run.log

cd "$script_dir"

echo "Ran on $(date)" > $log_file

$pipenv install >> $log_file
$pipenv run python . >> $log_file

echo "Generating cache..." >> $log_file

if [ -z $MYSQL_PASSWORD ]; then
    mysql -u $MYSQL_USERNAME $MYSQL_DATABASE < "$script_dir/database/dwd/generate_cache.sql"
else
    mysql -u $MYSQL_USERNAME -p$MYSQL_PASSWORD $MYSQL_DATABASE < "$script_dir/database/dwd/generate_cache.sql"
fi

echo "Done" >> $log_file
