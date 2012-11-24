#!/bin/sh

phantomjs bin/join_click_wifi.js | xargs wget -O -
