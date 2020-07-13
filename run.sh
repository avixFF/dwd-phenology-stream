#!/bin/bash

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
pipenv=/usr/local/bin/pipenv
log_file=run.log

cd "$script_dir"

echo "Ran on $(date)" > $log_file

$pipenv install >> $log_file
$pipenv run python . >> $log_file
