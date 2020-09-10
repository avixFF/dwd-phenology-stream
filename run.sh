#!/bin/bash

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)

cd "$script_dir"

# import .env
if [ -f .env ]; then
    export $(egrep -v '^#' .env | xargs)
fi

if [ -f .run.lock ]; then
    exit
fi

touch .run.lock

if [ ! -f .init ]; then
    python . --migrate database.migrations.dwd.CreateTables
    mysql -u $MYSQL_USERNAME $MYSQL_DATABASE < "$script_dir/database/dwd/weights.sql"
    touch .init
fi

echo "Ran on $(date)"

python .

echo "Generating cache..."

if [ -z $MYSQL_PASSWORD ]; then
    mysql -u $MYSQL_USERNAME $MYSQL_DATABASE < "$script_dir/database/dwd/generate_cache.sql"
else
    mysql -u $MYSQL_USERNAME -p$MYSQL_PASSWORD $MYSQL_DATABASE < "$script_dir/database/dwd/generate_cache.sql"
fi

echo "Done"

rm -f .run.lock
