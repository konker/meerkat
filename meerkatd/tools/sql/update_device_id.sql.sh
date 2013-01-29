#!/bin/sh

# update_device_id.sql.sh
#
# Copyright 2013 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#
#
# populate device_id field with the given value

VAL="''"
if [ "$1" == "NULL" ]; then
    VAL=$1
elif [ -n "$1" ]; then
    VAL="'$1'"
fi

echo "UPDATE probe_data SET device_id = $VAL;"

