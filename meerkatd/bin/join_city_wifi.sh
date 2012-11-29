#!/bin/sh

sudo wpa_cli select_network 3

curl --data "buttonClicked=4&err_flag=0&err_msg=&info_flag=0&info_msg=&redirect_url=ipv4.0-9.fi/" http://webauth.hel.fi/login.html
