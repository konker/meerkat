#!/bin/sh

LEN=$1
if [ -z "$1" ]; then
    LEN=60
fi
TICK=$(($LEN/4))

(exec sleep $TICK)
echo -n "{\"status\":\"OK\",\"data\":\"slept for $TICK seconds - 1\"}"
(exec sleep $TICK)
echo -n "{\"status\":\"OK\",\"data\":\"slept for $TICK seconds - 2\"}"
(exec sleep $TICK)
echo -n "{\"status\":\"OK\",\"data\":\"slept for $TICK seconds - 3\"}"
(exec sleep $TICK)
echo -n "{\"status\":\"END\",\"data\":\"slept for $LEN seconds\"}"
