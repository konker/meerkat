#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probe.wifi_client_scan
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import json
from scapy.all import *

MANAGEMENT_FRAME_TYPE = 0
MANAGEMENT_FRAME_SUBTYPES = (0, 2, 4)

unique = []
iface  = 'mon0'

def main():
    sniff(iface=iface, prn=sniffCallback)
    #sys.stdout.write(json.dumps(unique))


def sniffCallback(p): 
    if p.haslayer(Dot11):
        if p.type == MANAGEMENT_FRAME_TYPE and \
                p.subtype in MANAGEMENT_FRAME_SUBTYPES:
            if p.addr2 not in unique:
                unique.append(p.addr2)

                sys.stdout.write(json.dumps({'MAC_Address': p.addr2}))
                sys.stdout.flush()


if __name__ == '__main__':
    main()

