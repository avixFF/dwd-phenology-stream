#!/bin/bash

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
pipenv=/usr/local/bin/pipenv

cd "$script_dir"

# import .env
if [ -f .env ]; then
    export $(egrep -v '^#' .env | xargs)
fi

echo "Ran on $(date)"

$pipenv install
$pipenv run python .

echo "Generating cache..."

if [ -z $MYSQL_PASSWORD ]; then
    mysql -u $MYSQL_USERNAME $MYSQL_DATABASE < "$script_dir/database/dwd/generate_cache.sql"
else
    mysql -u $MYSQL_USERNAME -p$MYSQL_PASSWORD $MYSQL_DATABASE < "$script_dir/database/dwd/generate_cache.sql"
fi

echo "Done"
