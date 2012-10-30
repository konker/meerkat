#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probe.wifi_ap_scan
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import json
from scapy.all import *

unique = []

def main():
    sniff(iface="wlan0", prn=sniffBeacon)
    #sniff(iface="wlan0", filter="tcp port 80", prn=sniffBeacon)
    #sniff(iface="wlan0", prn=lambda x:x.sprintf("{Dot11Beacon:%Dot11.addr3%\t%Dot11Beacon.info%\t%PrismHeader.channel%\tDot11Beacon.cap%}"))

    print json.dumps(unique)


def sniffBeacon(p): 
    #print dir(p)
    #print p.summary
    #print p.haslayer(Dot11Beacon)
    #sys.exit()
    if ( (p.haslayer(Dot11Beacon) or p.haslayer(Dot11ProbeResp)) 
                 and not aps.has_key(p[Dot11].addr3)):
    #if p.haslayer(Dot11Beacon):
        if unique.count(p.addr2) == 0:
            unique.append(p.addr2)
            print p.sprintf("%Dot11.addr2%[%Dot11Elt.info%|%Dot11Beacon.cap%]")


if __name__ == '__main__':
    main()

