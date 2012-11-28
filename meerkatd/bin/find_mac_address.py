#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# find_mac_address.py
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import time
from scapy.all import *

MANAGEMENT_FRAME_TYPE = 0
MANAGEMENT_FRAME_SUBTYPES = (0, 2, 4)

iface  = 'mon0'
start = time.time()

def main():
    sniff(iface=iface, prn=sniffCallback)


def sniffCallback(p): 
    mac_addr = sys.argv[1]

    if p.haslayer(Dot11):
        if p.type == MANAGEMENT_FRAME_TYPE and \
                p.subtype in MANAGEMENT_FRAME_SUBTYPES:
            if p.addr2 == mac_addr:
                print "!!Found: %s in %s secs." % (p.addr2, (time.time() - start))
                sys.exit(0)
            else:
                print "Rejected: %s" % p.addr2


if __name__ == '__main__':
    main()

