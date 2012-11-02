#!/bin/sh

LEN=$1
if [ -z "$1" ]; then
    LEN=60
fi

sleep $LEN
echo -n "slept for $LEN seconds"
