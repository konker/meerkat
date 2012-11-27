#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# meerkat.probes.wifi_http_scan
#
# Copyright 2012 Konrad Markus
#
# Author: Konrad Markus <konker@gmail.com>
#

import sys
import re
import json
from scapy.all import *

MANAGEMENT_FRAME_TYPE = 0
MANAGEMENT_FRAME_SUBTYPES = (0, 2, 4)
FILTER = 'tcp port 80'

headers_re = re.compile("\r\n\r\n")
cookie_re = re.compile("cookie:.*\r\n", re.IGNORECASE)
unique = []
iface  = 'mon0'

def main():
    #sniff(iface=iface, filter=FILTER, prn=sniffCallback)
    sniff(iface=iface, prn=sniffCallback)


def sniffCallback(p): 
    if p.type != MANAGEMENT_FRAME_TYPE:
        #if 'SSID' in p and p['SSID'] == 'aalto open':
        if 'IP' in p and hasattr(p, 'load'):
            if 'HTTP' in p.load:
                if p.load.startswith('GET') or p.load.startswith('POST'):
                    print p.addr1
                    print p.src
                    print strip_cookies(get_headers(p))
                    print '---'


def strip_cookies(headers):
    return cookie_re.sub("Cookie: [REMOVED]\r\n", headers)


def get_headers(p):
    return headers_re.split(p.load)[0]

    '''
    if p.haslayer(Dot11):
        if p.type == MANAGEMENT_FRAME_TYPE and \
                p.subtype in MANAGEMENT_FRAME_SUBTYPES:
            if p.addr2 not in unique:
                unique.append(p.addr2)

                sys.stdout.write(json.dumps({'MAC_Address': p.addr2}))
                sys.stdout.flush()
    '''

if __name__ == '__main__':
    main()

