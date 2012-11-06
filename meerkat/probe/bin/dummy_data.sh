#!/bin/sh

CHARS=$1
if [ -z "$1" ]; then
    CHARS=64
fi

#echo `tr -dc A-Za-z0-9 </dev/urandom |  head -c $CHARS`
#DUMMY=`tr -dc A-Za-z0-9 </dev/urandom |  head -c $CHARS`
#echo -n $DUMMY
exec tr -dc A-Za-z0-9 </dev/urandom |  head -c $CHARS
#echo -n "DUMMY DATA"
