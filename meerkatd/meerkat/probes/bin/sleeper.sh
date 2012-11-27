#!/bin/sh

LEN=$1
if [ -z "$1" ]; then
    LEN=60
fi

exec sleep $LEN
echo -n "{\"status\":\"END\",\"data\":\"slept for $LEN seconds\"}"
