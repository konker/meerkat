#!/bin/sh

NETWORK=`wpa_cli list_networks | grep CURRENT | cut -c 1`
airmon-ng start wlan1 
wpa_cli select_network $NETWORK
