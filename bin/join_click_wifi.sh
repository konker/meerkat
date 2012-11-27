#!/bin/bash

OUT=`DISPLAY=:0 pyphantomjs bin/join_click_wifi.js`
#OUT=`phantomjs bin/join_click_wifi.js`
if [[ $OUT == "http://*" ]]; then
    wget -q -O - $OUT
    exec $0
else
    echo "OK"
fi
