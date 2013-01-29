#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probes.wifi_client_scan
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import json
import array
from scapy.all import *

MANAGEMENT_FRAME_TYPE = 0
MANAGEMENT_FRAME_SUBTYPES = (0, 2, 4)

#unique = []
iface  = 'mon0'


def main():
    sniff(iface=iface, prn=sniffCallback)


def sniffCallback(p): 
    if p.haslayer(Dot11):
        if p.type == MANAGEMENT_FRAME_TYPE and \
                p.subtype in MANAGEMENT_FRAME_SUBTYPES:

            '''
            if p.addr2 not in unique:
                unique.append(p.addr2)
            '''
            sys.stdout.write(json.dumps({
                "MAC_Address": p.addr2,
                "Destination": p.addr1,
                "SSID": p.getlayer(Dot11Elt, 1).info,
                "Subtype": p.subtype,
                "Signal_dBm": array.array('b', p.getlayer(RadioTap).notdecoded)[6],
                "Time_UTC": p.sprintf("%.time%")
            }))
            sys.stdout.write("\n")
            sys.stdout.flush()


if __name__ == '__main__':
    main()

