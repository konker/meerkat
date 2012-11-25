#!/bin/bash

PHANTOMJS=`which phantomjs`
if [ -z "$PHANTOMJS" ]; then
    export DISPLAY=:0
    PHANTOMJS="pyphantomjs"
else
    PHANTOMJS="phantomjs"
fi

HERE=`dirname "$0"`
echo $HERE
#OUT=`DISPLAY=:0 pyphantomjs bin/join_click_wifi.js`
OUT=`$PHANTOMJS $HERE/join_click_wifi.js`
if [[ $OUT == http:* ]]; then
    echo $OUT
    wget -q -O - $OUT
    exec $0
else
    echo "OK"
fi
