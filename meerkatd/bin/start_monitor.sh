#!/bin/sh

INTERFACE=$1
if [ -z "$INTERFACE" ]; then
    INTERFACE=wlan1
fi

NETWORK=`wpa_cli list_networks | grep CURRENT | cut -c 1`

airmon-ng start $INTERFACE 
wpa_cli select_network $NETWORK
