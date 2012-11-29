#!/bin/sh

# Hack which seems to get the GPS to work with NTPD
sudo killall gpsd
sudo /usr/sbin/gpsd /dev/ttyUSB0
sudo killall gpsd
sudo /usr/sbin/gpsd /dev/ttyUSB0
gpspipe -n 20 -r
