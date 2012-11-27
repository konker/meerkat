#!/bin/sh

# Hack in case kickstart_gps hack fails
sudo killall gpsd
sudo killall gpspipe
ps ax | grep gps
