#!/bin/sh

# update_latlong.sql.sh
#
# Copyright 2013 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#
#
# populate latitude and longitude fields with the given values

VAL1="''"
if [ "$1" == "NULL" ]; then
    VAL1=$1
elif [ -n "$1" ]; then
    VAL1="'$1'"
fi

VAL2="''"
if [ "$2" == "NULL" ]; then
    VAL2=$2
elif [ -n "$2" ]; then
    VAL2="'$2'"
fi

echo "UPDATE probe_data SET latitude = $VAL1, longitude = $VAL2;"

